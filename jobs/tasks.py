import logging
import httpx
from datetime import datetime

from django.core.serializers import serialize
from celery import shared_task 

from .models import CronJob, CronJobLog

logger = logging.getLogger(__name__)

@shared_task
def execute_job(id):
    job_exists = CronJob.objects.filter(pk=id).exists()  # Check if any matching object exists
    if job_exists:
        job = CronJob.objects.get(pk=id)
        response = httpx.get(job.url)
        response_text = response.text
        new_log_entry = CronJobLog(
            cronjob=job,
            execution_time=datetime.now(),
            status=True,
            output=response_text
        )
        new_log_entry.save()

        logger.info("GET Response: {}".format(response_text))
        logger.info("Execute job {}!".format(job.name))
    else:
        logger.error("Job with id {} does not exist!".format(id))