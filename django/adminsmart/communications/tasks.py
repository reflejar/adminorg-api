"""Celery tasks."""

# Django
from django.core.mail import EmailMultiAlternatives

# Celery
from celery.decorators import task

@task(name="send_emails")
def send_emails(from_email, destinations, subject, html_string, file_paths=[]):
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


