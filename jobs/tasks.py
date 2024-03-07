from .models import CronJob

def execute_job(id):
    job_exists = CronJob.objects.filter(pk=id)
    if job_exists:
        job = job_exists.get()
        print(job.id)
        print(job.name)
        print(job.url)
    print("Execute job {}!".format(id))
