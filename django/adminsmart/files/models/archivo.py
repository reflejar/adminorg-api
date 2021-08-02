from django.db import models
from django.apps import apps

from adminsmart.utils.models import BaseModel
from adminsmart.files.models import Carpeta

class Archivo(BaseModel):

	"""
	Modelo de las carpetas de archivos
	Las carpetas pueden tener carpetas dentro
	"""

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(blank=True, null=True)
	carpeta = models.ForeignKey(Carpeta, blank=True, null=True, related_name="archivos", on_delete=models.SET_NULL)
	ubicacion = models.FileField(upload_to="archivos/", blank=True, null=True)


	def __str__(self):
		return self.nombre

	def get_model(self, nombre):
		return apps.get_model('files', nombre)
