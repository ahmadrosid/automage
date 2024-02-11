from django.contrib import admin
from .models import CronJob, CronJobLog

admin.site.register(CronJob)
admin.site.register(CronJobLog)
