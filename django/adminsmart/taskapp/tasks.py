"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django_afip.models import ReceiptType

# Models
from adminsmart.users.models import User, Perfil
from adminsmart.utils.models import Comunidad
from adminsmart.operative.models import Documento
# from adminsmart.operative.serializers import MasivoClienteModelSerializer

# Celery
from celery.decorators import task, periodic_task

# Utilities
import jwt
import time
from datetime import timedelta

@task(name="facturacion_masiva")
def facturacion_masiva(data, context):

	print("hola")
	# context['receipt_type'] = ReceiptType.objects.get(description=context['receipt_type'])
	# context['comunidad'] = Comunidad.objects.get(id=context['comunidad'])

	# serializer = MasivoClienteModelSerializer(data=data, context=context)
	# serializer.is_valid(raise_exception=True)
	# serializer.save()

@task(name="hacer_pdfs")
def hacer_pdfs(docs_id):
	documentos = Documento.objects.filter(id__in=docs_id)
	for d in documentos:
		d.hacer_pdf()

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