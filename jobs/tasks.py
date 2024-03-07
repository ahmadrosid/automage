import logging
from .models import CronJob

logger = logging.getLogger(__name__)

def execute_job(id):
    job_exists = CronJob.objects.filter(pk=id)
    if job_exists:
        job = job_exists.get()
        logger.info(job)
    logger.info("Execute job {}!".format(id))
