from django.db import models
from django.contrib.auth.models import User


class CronJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=255)
    schedule = models.CharField(max_length=100)  # You can use a CharField for storing cron expression

    def __str__(self):
        return self.name


class CronJobLog(models.Model):
    cronjob = models.ForeignKey(CronJob, on_delete=models.CASCADE)
    execution_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    output = models.TextField()

    def __str__(self):
        return f"Execution of '{self.cronjob.name}' at {self.execution_time} {'(Success)' if self.status else '(Failure)'}"
