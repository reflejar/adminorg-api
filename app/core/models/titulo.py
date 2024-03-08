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

	def get_model(self, nombre):
			return apps.get_model('operative', nombre)

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

	def estado_cuenta(self, fecha=None):
		fecha = fecha if fecha else date.today()
		documentos = self.get_model('Documento').objects.filter(
				operaciones__cuenta__titulo__in=self.grupo, 
				# fecha__lte=fecha,
			).order_by('receipt').distinct('receipt')
		return self.get_model('Documento').objects.filter(
				id__in=documentos, 
				# fecha__lte=fecha,
			).select_related(
				"destinatario", 
				"destinatario__perfil", # Para el nombre de la cuenta
				"destinatario__naturaleza",
				"receipt", 
				"receipt__receipt_type", 
			).prefetch_related(
				"operaciones",
				"operaciones__cuenta",
				"operaciones__cuenta__naturaleza",
				"operaciones__vinculos",
				"operaciones__vinculos__cuenta",
				"operaciones__vinculos__cuenta__naturaleza",
			).order_by('fecha_operacion', 'id')



