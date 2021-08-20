from decimal import Decimal
from datetime import datetime, date, timedelta

from django.db import models

from adminsmart.utils.models import BaseModel
from adminsmart.operative.models import Cuenta, Metodo, Documento

class PreOperacion(BaseModel):

	"""
		Modelo de de operaciones
		Representa la operacion contable en su minima expresion
		Es la tabla madre donde se vuelcan todas las operaciones de las comunidades
	"""

	fecha = models.DateField(blank=True, null=True) # Fecha principal y contable. Con ella se ordenan las operaciones/evaluar eliminar
	fecha_indicativa = models.DateField(blank=True, null=True) # Fecha indicativa de periodo para diversas cuestiones/evaluar eliminar
	cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name="operaciones")
	cantidad = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
	valor = models.DecimalField(max_digits=9, decimal_places=2)
	vinculo = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="vinculos")
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

	def concepto(self):
		""" Devuelve la Cuenta(ingreso) por la que se creó el credito """

		# Por ahora no genera concepto si la operacion no es de un cliente o un dominio
		if not self.naturaleza in ['cliente', "dominio"]:
			return ""
		
		# conceptos = self.vinculos.filter(cuenta__naturaleza__nombre__in=["ingreso", "gasto", "caja"]) # Tambien está gasto para que tome "descuento" en el estado de cuenta
		# Esto se hace asi porque el prefetch_related ya trajo todos
		# Si se hace filtrando se duplican las consultas a DB
		conceptos = list(filter(lambda x: x.naturaleza in ["ingreso", "gasto", "caja"], self.vinculos.all()))
		if not (conceptos) and self.vinculo:
			# Unico momento donde efectivamente tiene que hacer una consulta SQL
			conceptos = list(filter(lambda x: x.naturaleza in ["ingreso", "gasto", "caja"], self.vinculo.vinculos.all()))
		if conceptos:
			return conceptos[0].cuenta
		return ""

		# conceptos = self.vinculos.all()
		# if not any([True if o.naturaleza() in ["ingreso", "gasto", "caja"] else False  for o in conceptos]):
		# 	return ""
		# if not conceptos:
		# 	if self.vinculo:
		# 		conceptos = self.vinculo.vinculos.all()
		# 		if not any([True if o.naturaleza() in ["ingreso", "gasto", "caja"] else False  for o in conceptos]):
		# 			return ""
		# 		return conceptos[0].cuenta
		# 	return ""
		# return conceptos[0].cuenta


	def periodo(self):
		# return "{}-{}".format(str(self.fecha_indicativa.year), self.fecha_indicativa.month)
		if not self.fecha_indicativa:
			return ""
		return self.fecha_indicativa.strftime("%Y-%m")

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


	def retencion(self):
		""" Devuelve la Metodo(retencion) por la que se creó el debito """
		return self.cuenta.metodos.filter(naturaleza="retencion", nombre=self.detalle).first()

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

	def pagos_interes(self, fecha=None):
		"""
			Retorna QUERYSET de pagos realizados de interes
		"""
		fecha = fecha if fecha else date.today()
		cuentas_intereses = Cuenta.all_objects.filter(comunidad=self.comunidad, taxon__nombre="interes_predeterminado")
		return Operacion.objects.filter(
			vinculo=self, 
			cuenta=self.cuenta, 
			vinculos__cuenta__in=cuentas_intereses, 
			fecha__lte=fecha, 
			documento__fecha_anulacion__isnull=True
			).order_by('fecha')		

	def pago_interes(self, fecha=None):
		"""
			Retorna VALOR de Pago total de intereses
		"""		
		fecha = fecha if fecha else date.today()
		calculo = self.pagos_interes(fecha=fecha).aggregate(calculo=models.Sum('valor'))['calculo'] or 0
		return abs(calculo)

	def pago_total(self, fecha=None):
		"""
			Retorna VALOR del Pago total de capital e interes
		"""
		fecha = fecha if fecha else date.today()
		return self.pago_capital(fecha=fecha) + self.pago_interes(fecha=fecha)


	def interes(self, fecha=None, condonacion=False):
		"""
			Retorna el calculo de interes a la fecha
		"""
		fecha = fecha if fecha else date.today()
		calculo = 0
		if condonacion:
			return calculo
		try:
			interes = self.metodos.get(naturaleza='interes')
		except:
			return calculo

		if self.fecha_vencimiento:
			if fecha > self.fecha_vencimiento:
				tasa = interes.monto
				reconocimiento = interes.reconocimiento
				base_calculo = interes.base_calculo
				
				pagos = list(self.pagos_capital(fecha=fecha))
				if pagos: # No se deberan restar los intereses pagados (salvo los posteriores que no hayan alcanzado el capital).
					fecha_calculo = pagos[-1].fecha if pagos[-1].fecha >= self.fecha_vencimiento else self.fecha_vencimiento
					bruto = self.subtotal(fecha=fecha_calculo)
					periodos = (fecha - fecha_calculo).days // reconocimiento # Se utiliza como fecha para el calculo de los periodos la del ultimo pago.
					# if periodos == 0 and fecha_calculo == date.today():
					# 	periodos = -1 # Esto se hace por si se paga parcial intereses + capital => abajo se le suma y queda periodos = 0
				else: # Si no se realizo pago de capital, el interes es el total desde la fecha inicial. Se debera posteriormente restar los intereses pagados.
					bruto = self.subtotal(fecha=self.fecha_vencimiento)
					periodos = (fecha - self.fecha_vencimiento).days // reconocimiento

				if reconocimiento != 1: # por si se elije un reconocimiento distinto de 1, para agararse el interes aun no generado
					periodos += 1
				
				calculo = round((bruto*tasa*periodos)/(100*base_calculo//reconocimiento), 2)

				if calculo < 0:
					calculo = 0
					
		return Decimal("%.2f" % calculo)		

	def descuento(self, fecha=None, condonacion=False):
		"""
			Retorna el calculo de descuento a la fecha
		"""		
		fecha = fecha if fecha else date.today()
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


	def subtotal(self, fecha=None):
		"""
			Retorna siempre positivo
		"""
		fecha = fecha if fecha else date.today()
		return abs(self.valor) - abs(self.pago_capital(fecha=fecha))
	
	def saldo(self, fecha=None, condonacion=False):
		"""
			Retorna siempre positivo el saldo adeudado a la fecha
		"""
		fecha = fecha if fecha else date.today()
		return self.subtotal(fecha=fecha) + self.interes(fecha=fecha, condonacion=condonacion) - self.descuento(fecha=fecha, condonacion=condonacion)


	def interes_generado(self, fecha=None):
		"""
			Retorna VALOR del interes generado total a la fecha.
			Tanto lo que se pago como lo que aun no
		"""				
		fecha = fecha if fecha else date.today()
		return self.interes(fecha=fecha) - self.pago_interes(fecha=fecha)
	
