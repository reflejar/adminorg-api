from decimal import Decimal
from datetime import datetime, date, timedelta

from django.db import models
from django.apps import apps

from utils.models import BaseModel
from core.models import Cuenta, Documento

class Operacion(BaseModel):

	"""
		Modelo de de operaciones
		Representa la operacion contable en su minima expresion
		Es la tabla madre donde se vuelcan todas las operaciones de las comunidades
	"""

	fecha = models.DateField(blank=True, null=True) # Fecha principal y contable. Con ella se ordenan las operaciones/evaluar eliminar
	periodo = models.DateField(blank=True, null=True) # Fecha indicativa de periodo para diversas cuestiones/evaluar eliminar
	asiento = models.CharField(max_length=30)
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="operaciones")
	concepto = models.ForeignKey(Cuenta, blank=True, null=True, on_delete=models.PROTECT, related_name="conceptos")
	documento = models.ForeignKey(Documento, blank=True, null=True, on_delete=models.PROTECT, related_name="operaciones")
	cantidad = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	valor = models.DecimalField(max_digits=9, decimal_places=2)
	vinculo = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="vinculos")
	fecha_vencimiento = models.DateField(blank=True, null=True)
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

	@property
	def debe(self):
		""" Devuelve el debe """
		return self.valor if self.valor > 0 else 0
	
	@property
	def haber(self):
		""" Devuelve el haber """
		return -self.valor if self.valor < 0 else 0		

	def destinatario(self):
		""" Devuelve la Cuenta(cliente, dominio) por la que se creó el credito """
		return self.cuenta


	def origen(self):
		return self.vinculo

	def causante(self):
		if self.documento.destinatario:
			return self.documento.destinatario.naturaleza.nombre
		if self.documento.receipt.receipt_type.code == "303":
			return "caja"
		if self.documento.receipt.receipt_type.code == "400":
			return "asiento"

	def titulo(self):
		return self.cuenta.titulo



	# Funciones muestrales
	def pagos_capital(self, fecha=None):
		"""
			Retorna QUERYSET de pagos realizados de capital
		"""
		fecha = fecha if fecha else date.today()
		cuentas_intereses = Cuenta.all_objects.filter(comunidad=self.comunidad, taxon__nombre="interes_predeterminado")
		return Operacion.objects.filter(
				vinculo=self, 
				cuenta=self.cuenta, 
				fecha__lte=fecha, 
				documento__fecha_anulacion__isnull=True
			).exclude(vinculos__cuenta__in=cuentas_intereses).order_by('fecha')

	def pago_capital(self, fecha=None):
		"""
			Retorna VALOR de Pago total del capital
		"""
		fecha = fecha if fecha else date.today()
		calculo = self.pagos_capital(fecha=fecha).aggregate(calculo=models.Sum('valor'))['calculo'] or 0
		return abs(calculo)




	def subtotal(self, fecha=None):
		"""
			Retorna siempre positivo
		"""
		fecha = fecha if fecha else date.today()
		return abs(self.valor) - abs(self.pago_capital(fecha=fecha))
