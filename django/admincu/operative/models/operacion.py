from decimal import Decimal
from datetime import datetime, date, timedelta

from django.db import models

from admincu.utils.models import BaseModel
from admincu.operative.models import Cuenta, Metodo, Documento

class Operacion(BaseModel):

	"""
		Modelo de de operaciones
		Representa la operacion contable en su minima expresion
		Es la tabla madre donde se vuelcan todas las operaciones de las comunidades
	"""

	fecha = models.DateField(blank=True, null=True) # Fecha principal y contable. Con ella se ordenan las operaciones/evaluar eliminar
	fecha_indicativa = models.DateField(blank=True, null=True) # Fecha indicativa de periodo para diversas cuestiones/evaluar eliminar
	asiento = models.CharField(max_length=30)
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="operaciones")
	documento = models.ForeignKey(Documento, blank=True, null=True, on_delete=models.PROTECT, related_name="operaciones")
	cantidad = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	valor = models.DecimalField(max_digits=9, decimal_places=2)
	vinculo = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="vinculos")
	metodos = models.ManyToManyField(Metodo, blank=True)
	fecha_vencimiento = models.DateField(blank=True, null=True)
	fecha_gracia = models.DateField(blank=True, null=True)
	detalle = models.CharField(max_length=150, blank=True, null=True)
	descripcion = models.CharField(max_length=150, blank=True, null=True)
	# Agregar cantidades, y magnitudes fisicas



	# Funciones Serializadoras
	def monto(self):
		""" Devuelve el valor en positivo siempre """
		# if self.cuenta.naturaleza.nombre in ['cliente', 'dominio'] and self.vinculo:
		# 	return abs(Operacion.objects.filter(asiento=self.asiento, vinculo=self.vinculo).aggregate(calculo=models.Sum('valor'))['calculo'])
		return abs(self.valor)

	def debe(self):
		""" Devuelve el debe """
		return self.valor if self.valor > 0 else 0

	def haber(self):
		""" Devuelve el haber """
		return -self.valor if self.valor < 0 else 0		

	def destinatario(self):
		""" Devuelve la Cuenta(cliente, dominio) por la que se creó el credito """
		return self.cuenta

	def concepto(self):
		""" Devuelve la Cuenta(ingreso) por la que se creó el credito """
		conceptos = self.vinculos.filter(cuenta__naturaleza__nombre__in=["ingreso", "gasto", "caja"]) # Tambien está gasto para que tome "descuento" en el estado de cuenta
		if not conceptos:
			if self.vinculo:
				conceptos = self.vinculo.vinculos.filter(cuenta__naturaleza__nombre__in=["ingreso", "gasto", "caja"])
				if conceptos:
					return conceptos.first().cuenta
			return None
		return conceptos.first().cuenta

	def retencion(self):
		""" Devuelve la Metodo(retencion) por la que se creó el debito """
		return self.cuenta.metodos.filter(naturaleza="retencion", nombre=self.detalle).first()

	# Funciones muestrales
	def pagos_capital(self, fecha=date.today()):
		"""
			Retorna QUERYSET de pagos realizados de capital
		"""
		cuentas_intereses = Cuenta.all_objects.filter(comunidad=self.comunidad, taxon__nombre="interes_predeterminado")
		return Operacion.objects.filter(
				vinculo=self, 
				cuenta=self.cuenta, 
				fecha__lte=fecha, 
				documento__fecha_anulacion__isnull=True
			).exclude(vinculos__cuenta__in=cuentas_intereses).order_by('fecha')

	def pago_capital(self, fecha=date.today()):
		"""
			Retorna VALOR de Pago total del capital
		"""
		calculo = self.pagos_capital(fecha=fecha).aggregate(calculo=models.Sum('valor'))['calculo'] or 0
		
		return abs(calculo)

	def pagos_interes(self, fecha=date.today()):
		"""
			Retorna QUERYSET de pagos realizados de interes
		"""
		cuentas_intereses = Cuenta.all_objects.filter(comunidad=self.comunidad, taxon__nombre="interes_predeterminado")
		return Operacion.objects.filter(
			vinculo=self, 
			cuenta=self.cuenta, 
			vinculos__cuenta__in=cuentas_intereses, 
			fecha__lte=fecha, 
			documento__fecha_anulacion__isnull=True
			).order_by('fecha')		

	def pago_interes(self, fecha=date.today()):
		"""
			Retorna VALOR de Pago total de intereses
		"""		
		calculo = self.pagos_interes(fecha=fecha).aggregate(calculo=models.Sum('valor'))['calculo'] or 0
		return abs(calculo)

	def pago_total(self, fecha=date.today()):
		"""
			Retorna VALOR del Pago total de capital e interes
		"""						
		return self.pago_capital(fecha=fecha) + self.pago_interes(fecha=fecha)


		
	def interes(self, fecha=date.today(), condonacion=False):
		"""
			Retorna el calculo de interes a la fecha
		"""
		calculo = 0
		if condonacion:
			return calculo
		try:
			interes = self.metodos.get(naturaleza='interes')
		except:
			return calculo

		if self.fecha_vencimiento:
			if fecha > self.fecha_vencimiento:
				pagos = list(self.pagos_capital(fecha=fecha))
				tasa = interes.monto
				reconocimiento = interes.reconocimiento
				base_calculo = interes.base_calculo
				
				if pagos: # No se deberan restar los intereses pagados (salvo los posteriores que no hayan alcanzado el capital).
					fecha_calculo = pagos[-1].fecha if pagos[-1].fecha >= self.fecha_vencimiento else self.fecha_vencimiento
					bruto = self.subtotal(fecha=fecha_calculo) 
					periodos = (fecha - fecha_calculo.days) // reconocimiento # Se utiliza como fecha para el calculo de los periodos la del ultimo pago.
				else: # Si no se realizo pago de capital, el interes es el total desde la fecha inicial. Se debera posteriormente restar los intereses pagados.
					bruto = self.subtotal(fecha=self.fecha_vencimiento)
					periodos = (fecha - self.fecha_vencimiento).days // reconocimiento

				if not reconocimiento == 1: # por si se elije un reconocimiento distinto de 1, para agararse el interes aun no generado
					periodos += 1
				calculo = round((bruto*tasa*periodos)/(100*base_calculo//reconocimiento), 2)

				pagos_interes = list(self.pagos_interes(fecha=fecha))
				for pago in pagos_interes: # Se restan los intereses pagados. 
					# credito = Operacion.objects.get(vinculo=self, cuenta=self.cuenta, vinculos__cuenta=self.concepto(), asiento=pago.asiento)
					credito = Operacion.objects.filter(vinculo=self, cuenta=self.cuenta, vinculos__cuenta=self.concepto(), asiento=pago.asiento)
					try: # No se restan si se ha producido un pago de capital en el asiento porque el interes es automaticamente calculado desde una fecha posterior.
						credito = Operacion.objects.get(vinculo=self, cuenta=self.cuenta, vinculos__cuenta=self.concepto(), asiento=pago.asiento)
					except: 
						calculo = calculo + pago.valor


				if calculo < 0:
					calculo = 0

		return Decimal("%.2f" % calculo)
		

	def descuento(self, fecha=date.today(), condonacion=False):
		"""
			Retorna el calculo de descuento a la fecha
		"""		
		calculo = 0
		if condonacion:
			return calculo
		try:
			descuento = self.metodos.get(naturaleza='descuento')
		except:
			return calculo 
			
		if self.fecha_gracia:
			if fecha <= self.fecha_gracia:
				if descuento.tipo == "fijo":
					calculo = round(descuento.monto, 2)
				else:
					capital = self.valor
					calculo = round(capital * descuento.monto / 100, 2)
		return Decimal("%.2f" % calculo)


	def subtotal(self, fecha=date.today()):
		"""
			Retorna siempre positivo
		"""

		return abs(self.valor) - abs(self.pago_capital(fecha=fecha))
	
	def saldo(self, fecha=date.today(), condonacion=False):
		"""
			Retorna siempre positivo el saldo adeudado a la fecha
		"""
		
		return self.subtotal(fecha=fecha) + self.interes(fecha=fecha, condonacion=condonacion) - self.descuento(fecha=fecha, condonacion=condonacion)


	def interes_generado(self, fecha=date.today()):
		"""
			Retorna VALOR del interes generado total a la fecha.
			Tanto lo que se pago como lo que aun no
		"""				
		return self.interes(fecha=fecha) - self.pago_interes(fecha=fecha)
	
	def periodo(self):
		# return "{}-{}".format(str(self.fecha_indicativa.year), self.fecha_indicativa.month)
		if not self.fecha_indicativa:
			return ""
		return self.fecha_indicativa.strftime("%Y-%m")

	def origen(self):
		return self.vinculo

	def causante(self):
		if self.documento.destinatario:
			return self.documento.destinatario.naturaleza
		if self.documento.receipt.receipt_type.code == "303":
			return "caja"
		if self.documento.receipt.receipt_type.code == "400":
			return "asiento"

	def titulo(self):
		return self.cuenta.titulo

	def naturaleza(self):
		return self.cuenta.naturaleza.nombre