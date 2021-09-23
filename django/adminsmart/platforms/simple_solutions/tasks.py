"""Celery tasks."""

# Django
from django.core.mail import EmailMultiAlternatives

# Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task

# Utilities
import jwt
import time
from datetime import timedelta


@periodic_task(name="send_ss", run_every=crontab(hour=4, minute=0))
def send_ss(from_email, destinations, subject, html_string, file_paths=[]):
	for email in destinations:
		msg = EmailMultiAlternatives(
			subject=subject,
			body="",
			from_email=from_email,
			to=[email],
		)
		msg.attach_alternative(html_string, "text/html")
		for f in file_paths:
			msg.attach_file(f)
		msg.send()


