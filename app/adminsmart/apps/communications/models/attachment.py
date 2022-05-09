# Django
from django.db import models

# Project
from adminsmart.apps.files.models import PDF, Archivo


class Attachment(models.Model):
	"""Adjuntos para el envio"""

	archivo = models.ForeignKey(Archivo, blank=True, null=True, on_delete=models.SET_NULL)
	pdf = models.ForeignKey(PDF, blank=True, null=True, on_delete=models.SET_NULL)

	@property
	def file(self):
		if self.archivo:
			return self.archivo
		else:
			return self.pdf

	@property
	def file_name(self):
		if self.archivo:
			return str(self.archivo.ubicacion)
		else:
			return str(self.pdf.location)
