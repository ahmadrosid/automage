run:
	python manage.py runserver

run_celery:
	celery -A automage worker -l INFO

run_celery_beat:
	celery -A automage beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
