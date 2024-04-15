from core.models import Operacion
from utils.generics.functions import *
from django_afip.models import CurrencyType
from core.models import Cuenta

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, comprobante, validated_data):
		self.comprobante = comprobante
		self.moneda_comprobante = comprobante.receipt.currency
		self.tipo_cambio = comprobante.receipt.currency_quote
		self.comunidad = comprobante.comunidad
		self.fecha_operacion = comprobante.fecha_operacion
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.cargas = validated_data['cargas']
		self.cobros = validated_data['cobros']
		self.descargas = validated_data['descargas']
		self.cargas_guardadas = []
		self.cobros_guardados = []
		self.descargas_guardadas = []
		self.direccion = self.comprobante.destinatario.direccion

		self.pesos = CurrencyType.objects.get(description="$ARS")
		self.rdo_tipo_cambio_pos = Cuenta.objects.get(naturaleza__nombre="ingreso", taxon__nombre='tipo_cambio')
		self.rdo_tipo_cambio_neg = Cuenta.objects.get(naturaleza__nombre="gasto", taxon__nombre='tipo_cambio')


	def hacer_cargas(self):
		for o in self.cargas:
			# Alta de la carga
			moneda = self.comprobante.destinatario.moneda or self.moneda_comprobante
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=self.comprobante.destinatario,
				concepto=o['concepto'],
				proyecto=o['proyecto'],
				cantidad=o['cantidad'],
				moneda=moneda,
				valor=o['total_pesos']*self.direccion if moneda.description == "$ARS" else o['monto']*self.direccion,
				tipo_cambio=1 if moneda.description == "$ARS" else self.tipo_cambio,
				total_pesos=o['total_pesos']*self.direccion,
				detalle=o['detalle'],
				periodo=self.fecha_operacion,
			))
			# Contracuenta de la carga
			original = o['monto'] * o['tipo_cambio'] # Tipo de cambio original
			real = o['monto'] * self.tipo_cambio # Tipo de cambio real
			dif = real - original   
			moneda = o['concepto'].moneda or self.moneda_comprobante
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['concepto'],
				concepto=self.comprobante.destinatario,
				proyecto=o['proyecto'],
				cantidad=o['cantidad'],
				moneda=moneda,
				valor=-original*self.direccion if moneda.description == "$ARS" else -o['monto']*self.direccion,
				tipo_cambio=1 if moneda.description == "$ARS" else o['tipo_cambio'],
				total_pesos=-original*self.direccion,
				detalle=o['detalle'],
				periodo=self.fecha_operacion,
			))
			if dif != 0:
				cuenta = self.rdo_tipo_cambio_pos if dif*self.direccion > 0 else self.rdo_tipo_cambio_neg			
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					comprobante = self.comprobante,
					asiento=self.identifier,
					cuenta=cuenta,
					concepto=self.comprobante.destinatario,
					proyecto=o['proyecto'],
					cantidad=o['cantidad'],
					moneda=self.pesos,
					valor=-dif*self.direccion,
					tipo_cambio=1,
					total_pesos=-dif*self.direccion,
					detalle=o['detalle'],
					periodo=self.fecha_operacion,
				))	


	def hacer_cobros(self):
		for o in self.cobros:
			deuda = o['monto'] * o['vinculo'].tipo_cambio
			pagado = o['monto'] * self.tipo_cambio
			dif = pagado - deuda
			self.cobros_guardados.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['vinculo'].cuenta,
				concepto=o['vinculo'].concepto,
				proyecto=o['vinculo'].proyecto,
				periodo=o['vinculo'].periodo,
				moneda=self.moneda_comprobante,
				valor=-o['monto']*self.direccion,
				tipo_cambio=self.tipo_cambio,
				total_pesos=-deuda*self.direccion,
				detalle=o['detalle'],
				vinculo=o['vinculo'],
			))
			# Diferencia por desfasaje del tipo de cambio 
			if dif != 0:
				cuenta = self.rdo_tipo_cambio_pos if dif*self.direccion > 0 else self.rdo_tipo_cambio_neg
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					comprobante = self.comprobante,
					asiento=self.identifier,
					cuenta=cuenta,
					concepto=o['vinculo'].concepto,
					proyecto=o['vinculo'].proyecto,
					periodo=o['vinculo'].periodo,
					moneda=self.pesos,
					valor=-dif*self.direccion,
					tipo_cambio=1,
					total_pesos=-dif*self.direccion,
					detalle=o['detalle'],
					vinculo=o['vinculo'],
				))							



	def hacer_descargas(self):
		for o in self.descargas:
			moneda = o['cuenta'].moneda or self.moneda_comprobante
			self.descargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['cuenta'],
				concepto=self.comprobante.destinatario,
				fecha_vencimiento=o['fecha_vencimiento'],
				moneda=moneda,
				valor=o['total_pesos']*self.direccion if moneda.description == "$ARS" else o['monto']*self.direccion,
				tipo_cambio=1 if moneda.description == "$ARS" else self.tipo_cambio,				
				total_pesos=o['total_pesos']*self.direccion,
				detalle=o['detalle'],
			))
		if self.descargas:
			for o in self.cargas_guardadas:
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					comprobante = self.comprobante,
					asiento=self.identifier,
					cuenta=o.cuenta,
					concepto=o.concepto,
					proyecto=o.proyecto,
					periodo=o.periodo,
					valor=-o.valor,
					moneda=self.moneda_comprobante,
					tipo_cambio=self.tipo_cambio,
					total_pesos=-o.valor*self.tipo_cambio,					
					detalle=o.detalle,
					vinculo=o,
				))			

	def create(self):

		self.hacer_cargas()

		self.hacer_cobros()
		
		self.hacer_descargas()