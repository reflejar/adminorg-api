# Models
from adminsmart.operative.models import Documento

# Celery
from celery.decorators import task

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