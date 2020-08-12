from django.db import models
from admincu.utils.models import BaseModel

class Titulo(BaseModel):

	"""
	Modelo de titulos de las cuentas
	Es para poder manejar CONTABLEMENTE los niveles de los rubros. 
	Las cuentas tienen SIEMPRE un solo titulo 
	"""
	nombre = models.CharField(max_length=100)
	# numero = models.IntegerField(blank=True, null=True)
	# supertitulo = models.ForeignKey('self', blank=True, null=True, related_name="subtitulos", on_delete=models.SET_NULL)

	def __str__(self):

		return self.nombre

