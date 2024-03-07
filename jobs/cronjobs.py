from django_cron import CronJobBase, Schedule

class ExecutionCronJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'jobs.schedules.write_file'

    def do(self):
        print("Job executed!")

