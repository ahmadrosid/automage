from .models import CronJob

def write_file(id):
    job_exists = CronJob.objects.filter(pk=id)
    if job_exists:
        job = job_exists.get()
        print(job.id)
        print(job.name)
        print(job.command)
    print("Execute job {}!".format(id))
