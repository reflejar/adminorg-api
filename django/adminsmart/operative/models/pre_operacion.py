from decimal import Decimal
from datetime import datetime, date, timedelta

from django.db import models

from adminsmart.utils.models import BaseModel
from adminsmart.operative.models import Cuenta, Metodo, Documento

class PreOperacion(BaseModel):

	"""
		Modelo de de Preoperaciones
		Representa la operacion contable en su minima expresion
		Es la tabla fantasma, donde se vuelcan todas las operaciones sin confirmar
	"""

	fecha_indicativa = models.DateField(blank=True, null=True) # Fecha indicativa de periodo para diversas cuestiones/evaluar eliminar
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="preoperaciones")
	cantidad = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	valor = models.DecimalField(max_digits=9, decimal_places=2)
	concepto = models.ForeignKey(Cuenta, blank=True, null=True, on_delete=models.SET_NULL, related_name="preconceptos")
	metodos = models.ManyToManyField(Metodo, blank=True)
	fecha_vencimiento = models.DateField(blank=True, null=True)
	fecha_gracia = models.DateField(blank=True, null=True)
	detalle = models.CharField(max_length=150, blank=True, null=True)
	descripcion = models.CharField(max_length=150, blank=True, null=True)

	# Funciones Serializadoras
	@property
	def naturaleza(self):
		return self.cuenta.naturaleza.nombre

	@property
	def monto(self):
		""" Devuelve el valor en positivo siempre """
		return abs(self.valor)

	def destinatario(self):
		""" Devuelve la Cuenta(cliente, dominio) por la que se creó el credito """
		return self.cuenta

	def periodo(self):
		# return "{}-{}".format(str(self.fecha_indicativa.year), self.fecha_indicativa.month)
		if not self.fecha_indicativa:
			return ""
		return self.fecha_indicativa.strftime("%Y-%m")

	def titulo(self):
		return self.cuenta.titulo

	def retencion(self):
		""" Devuelve la Metodo(retencion) por la que se creó el debito """
		return self.cuenta.metodos.filter(naturaleza="retencion", nombre=self.detalle).first()