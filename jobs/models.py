from django.db import models
from django.contrib.auth.models import User


class CronJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=255)
    schedule = models.CharField(max_length=100)  # You can use a CharField for storing cron expression

    def __str__(self):
        return self.name
