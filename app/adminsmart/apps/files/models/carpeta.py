from django.db import models
from django.apps import apps
from django.contrib.auth.models import Group

from adminsmart.apps.utils.models import BaseModel

class Carpeta(BaseModel):

	"""
	Modelo de las carpetas de archivos
	Las carpetas pueden tener carpetas dentro
	"""

	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(blank=True, null=True)
	supercarpeta = models.ForeignKey('self', blank=True, null=True, related_name="subcarpetas", on_delete=models.SET_NULL)
	exposicion = models.ManyToManyField(Group, blank=True)


	def __str__(self):
		return self.nombre

	def get_model(self, nombre):
		return apps.get_model('files', nombre)
