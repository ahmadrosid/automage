# AutoMage

Cronjobs scheduler with django.

![demo](./screenshot.png)

## Run Migrations

```bash
python manage.py migrate
python manage.py migrate django_apscheduler
python manage.py migrate jobs
```

## Run scheduler

```bash
celery -A automage worker -l INFO
```

```bash
celery -A automage beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
```