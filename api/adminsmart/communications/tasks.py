from datetime import timedelta

# Django
from django.utils import timezone

# Celery
from celery.decorators import periodic_task
from .models import Queue


@periodic_task(name="attend_queue", run_every=timedelta(seconds=30))
def attend_queue():
	now = timezone.now()
	for instance in Queue.objects.filter(execute_at__lt=now):
		instance.exec()
