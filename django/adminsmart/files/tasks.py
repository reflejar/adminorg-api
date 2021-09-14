from datetime import timedelta

# Models
from .models import PDF

# Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task


@periodic_task(name="delete_pdfs", run_every=crontab(hour=0, minute=0))
def delete_pdfs():
	for pdf in PDF.objects.filter(location__isnull=False):
		pdf.remove()