# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution, DjangoJob
from django_apscheduler import util

from jobs.models import CronJob
from jobs import schedules

logger = logging.getLogger(__name__)


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)

def get_job(id):
  return DjangoJob.objects.filter(pk=id)

def delete_job(job_id):
  try:
      obj = DjangoJob.objects.get(pk=job_id)
      obj.delete()
  except DjangoJob.DoesNotExist:
    logger.info("Failed to remove job with job_id '{}'.".format(job_id))

class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    jobs = CronJob.objects.all()
    for job in jobs:
      job_function = getattr(schedules, 'write_file')
      job_id = "job-{}".format(job.id)
      if get_job(job_id):
        delete_job(job_id)

      scheduler.add_job(
          func=job_function,
          trigger=CronTrigger.from_crontab(expr=job.schedule),
          id=job_id,
          name=job.name,
          args=[job.id],  # Pass any parameters needed for the job
      )

    scheduler.add_job(
      delete_old_job_executions,
      # trigger=CronTrigger(second="*/10"),
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")