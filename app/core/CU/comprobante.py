from core.models import Operacion
from utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, comprobante, validated_data):
		self.comprobante = comprobante
		self.moneda = comprobante.receipt.currency
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



	def hacer_cargas(self):
		for o in self.cargas:
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=self.comprobante.destinatario,
				concepto=o['concepto'],
				proyecto=o['proyecto'],
				cantidad=o['cantidad'],
				valor=o['monto']*self.direccion,
				moneda=self.moneda,
				tipo_cambio=self.tipo_cambio,
				total_pesos=o['monto']*self.direccion*self.tipo_cambio,
				detalle=o['detalle'],
				periodo=self.fecha_operacion,
			))
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['concepto'],
				proyecto=o['proyecto'],
				cantidad=o['cantidad'],
				valor=-o['monto']*self.direccion,
				moneda=self.moneda,
				tipo_cambio=self.tipo_cambio,
				total_pesos=-o['monto']*self.direccion*self.tipo_cambio,
				detalle=o['detalle'],
				periodo=self.fecha_operacion,
			))



	def hacer_cobros(self):
		for o in self.cobros:
			self.cobros_guardados.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['vinculo'].cuenta,
				concepto=o['vinculo'].concepto,
				proyecto=o['vinculo'].proyecto,
				periodo=o['vinculo'].periodo,
				valor=-o['monto']*self.direccion,
				moneda=self.moneda,
				tipo_cambio=self.tipo_cambio,
				total_pesos=-o['monto']*self.direccion*self.tipo_cambio,						
				detalle=o['detalle'],
				vinculo=o['vinculo'],
			))



	def hacer_descargas(self):
		for o in self.descargas:
			self.descargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				comprobante = self.comprobante,
				asiento=self.identifier,
				cuenta=o['cuenta'],
				fecha_vencimiento=o['fecha_vencimiento'],
				valor=o['monto']*self.direccion,
				moneda=self.moneda,
				tipo_cambio=self.tipo_cambio,
				total_pesos=o['monto']*self.direccion*self.tipo_cambio,
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
					moneda=self.moneda,
					tipo_cambio=self.tipo_cambio,
					total_pesos=-o.valor*self.tipo_cambio,					
					detalle=o.detalle,
					vinculo=o,
				))			

	def create(self):

		self.hacer_cargas()

		self.hacer_cobros()
		
		self.hacer_descargas()