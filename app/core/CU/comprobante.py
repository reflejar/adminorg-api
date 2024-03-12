from core.models import Operacion
from utils.generics.functions import *

class CU:
	'''Operacion de creditos realizada a cliente'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.fecha_operacion = documento.fecha_operacion
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.cargas = validated_data['cargas']
		self.cobros = validated_data['cobros']
		self.descargas = validated_data['descargas']
		self.cargas_guardadas = []
		self.cobros_guardados = []
		self.descargas_guardadas = []
		self.direccion = self.documento.destinatario.direccion



	def hacer_cargas(self):
		for o in self.cargas:
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=self.documento.destinatario,
				concepto=o['concepto'],
				cantidad=o['cantidad'],
				valor=o['monto']*self.direccion,
				detalle=o['detalle'],
				periodo=o['periodo'] or self.fecha_operacion,
				fecha_vencimiento=o['fecha_vencimiento'],
			))
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['concepto'],
				concepto=self.documento.destinatario,
				cantidad=o['cantidad'],
				valor=-o['monto']*self.direccion,
				detalle=o['detalle'],
				periodo=o['periodo'] or self.fecha_operacion,
				fecha_vencimiento=o['fecha_vencimiento'],
			))



	def hacer_cobros(self):
		for o in self.cobros:
			self.cobros_guardados.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['vinculo'].cuenta,
				concepto=o['vinculo'].concepto,
				periodo=o['vinculo'].periodo or self.fecha_operacion,
				valor=-o['monto']*self.direccion,
				detalle=o['detalle'],
				vinculo=o['vinculo'],
			))



	def hacer_descargas(self):
		for o in self.descargas:
			self.descargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['cuenta'],
				concepto=self.documento.destinatario,
				fecha_vencimiento=o['fecha_vencimiento'],
				valor=o['monto']*self.direccion,
				detalle=o['detalle'],
			))
		if self.descargas:
			for o in self.cargas_guardadas:
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento = self.documento,
					asiento=self.identifier,
					cuenta=o.cuenta,
					concepto=o.concepto,
					periodo=o.periodo,
					valor=-o.valor,
					detalle=o.detalle,
					vinculo=o,
				))			

	def create(self):

		self.hacer_cargas()

		self.hacer_cobros()
		
		self.hacer_descargas()