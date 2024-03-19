from datetime import date
from django.db import models
from utils.models import BaseModel
from django.apps import apps
from django.db.models import Q

class Titulo(BaseModel):

	"""
	Modelo de titulos de las cuentas
	Es para poder manejar CONTABLEMENTE los niveles de los rubros. 
	Las cuentas tienen SIEMPRE un solo titulo 
	"""
	nombre = models.CharField(max_length=100)
	numero = models.IntegerField(blank=True, null=True)
	supertitulo = models.ForeignKey('self', blank=True, null=True, related_name="subtitulos", on_delete=models.SET_NULL)
	predeterminado = models.ForeignKey("core.Naturaleza", blank=True, null=True, related_name="titulos", on_delete=models.SET_NULL)

	def __str__(self):

		return self.nombre

	@property
	def cuentas(self):
		"""Esto esta puesto aqui porque no se coloco oportunamente el related_name en el modelo de Cuenta"""
		return self.cuenta_set.all()

	@property
	def grupo(self):
		titulos = Titulo.objects.filter(
					Q(id=self.id) |
					Q(supertitulo=self) |
					Q(supertitulo__supertitulo=self) |
					Q(supertitulo__supertitulo__supertitulo=self) |
					Q(supertitulo__supertitulo__supertitulo__supertitulo=self)
		)
		return titulos

