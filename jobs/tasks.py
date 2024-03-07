import logging
from django.core.serializers import serialize
from celery import shared_task 

from .models import CronJob

logger = logging.getLogger(__name__)

@shared_task
def execute_job(id):
    job_exists = CronJob.objects.filter(pk=id).exists()  # Check if any matching object exists
    if job_exists:
        job = CronJob.objects.get(pk=id)
        data = serialize('json', [job])
        logger.info(data)
        logger.info("Execute job {}!".format(job.name))
    else:
        logger.error("Job with id {} does not exist!".format(id))