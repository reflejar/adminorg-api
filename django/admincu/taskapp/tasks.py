"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django_afip.models import ReceiptType

# Models
from admincu.users.models import User
from admincu.utils.models import Comunidad
from admincu.operative.models import Documento
# from admincu.operative.serializers import MasivoClienteModelSerializer

# Celery
from celery.decorators import task, periodic_task

# Utilities
import jwt
import time
from datetime import timedelta


def gen_verification_token(user):
	"""Create JWT token that the user can use to verify its account."""
	exp_date = timezone.now() + timedelta(days=3)
	payload = {
		'user': user.username,
		'exp': int(exp_date.timestamp()),
		'type': 'email_confirmation'
	}
	token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
	return token.decode()


@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
	"""Send account verification link to given user."""
	user = User.objects.get(pk=user_pk)
	verification_token = gen_verification_token(user)
	subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
	from_email = 'Comparte Ride <noreply@admin-cu.com>'
	content = render_to_string(
		'emails/users/account_verification.html',
		{'token': verification_token, 'user': user}
	)
	msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
	msg.attach_alternative(content, "text/html")
	msg.send()


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