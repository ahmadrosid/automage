from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .models import CronJob

def from_crontab(crontab_expression):
    """
    Convert a crontab-like expression into a CrontabSchedule object.
    """
    parts = crontab_expression.split()
    return CrontabSchedule.objects.create(
        minute=parts[0],
        hour=parts[1],
        day_of_month=parts[2],
        month_of_year=parts[3],
        day_of_week=parts[4],
    )

def add_to_scheduler(cron: CronJob):
    crontab_schedule = from_crontab(cron.schedule)
    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name="job-{}".format(cron.id),
        task="jobs.tasks.execute_job",
        args=[cron.id]
    )

def delete_scheduler(cron: CronJob):
    job = PeriodicTask.objects.filter(
        name="job-{}".format(cron.id),
    )

    if job.exists():
        job.delete()

def update_scheduler(cron: CronJob):
    delete_scheduler(cron)
    add_to_scheduler(cron)