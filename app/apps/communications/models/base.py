# Django
from django.db import models

# Project
from apps.utils.models import BaseModel
from .attachment import Attachment

class BaseCommunication(BaseModel):
	"""
	Modelo para almacenar los envios
	Base de cualquier comunicacion 
	Cuando salga de aqui un envio puede enviarse
	por mail o hacia las plataformas de comunicacion 
		a la fecha: simple_solutions, expensas_pagas (SE ELIMINARON PARA ADMINORG)
	"""

	addressee = models.ForeignKey('users.Perfil', on_delete=models.PROTECT)
	subject = models.CharField(max_length=150, blank=True, null=True)
	body = models.TextField(blank=True, null=True)
	attachments = models.ManyToManyField(Attachment, blank=True)
	observations = models.TextField(blank=True, null=True)
	client = models.CharField(max_length=300)

	class Meta:
		abstract = True
