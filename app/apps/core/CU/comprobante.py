from apps.core.models import Operacion
from apps.utils.generics.functions import *

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
		self.cajas = validated_data['cajas']
		self.resultados = validated_data['resultados']
		self.cargas_guardadas = []
		self.cobros_guardados = []
		self.cajas_guardadas = []
		self.resultados_guardados = []
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
				fecha_indicativa=o['periodo'] or self.fecha_operacion,
				fecha_gracia=o['fecha_gracia'],
				fecha_vencimiento=o['fecha_vencimiento'],
			))
			self.cargas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['concepto'],
				cantidad=o['cantidad'],
				valor=-o['monto']*self.direccion,
				detalle=o['detalle'],
				fecha_indicativa=o['periodo'] or self.fecha_operacion,
				fecha_gracia=o['fecha_gracia'],
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
				fecha_indicativa=o['vinculo'].fecha_indicativa or self.fecha_operacion,
				valor=-o['monto']*self.direccion,
				detalle=o['detalle'],
				vinculo=o['vinculo'],
			))



	def hacer_cajas(self):
		for o in self.cajas:
			self.cajas_guardadas.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['cuenta'],
				fecha_vencimiento=o['fecha_vencimiento'],
				valor=o['monto']*self.direccion,
				detalle=o['detalle'],
			))
		if self.cajas:
			for o in self.cargas_guardadas:
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento = self.documento,
					asiento=self.identifier,
					cuenta=o.cuenta,
					fecha_indicativa=o.fecha_indicativa,
					valor=-o.valor,
					detalle=o.detalle,
					vinculo=o,
				))			


	def hacer_resultados(self):
		for o in self.resultados:
			self.resultados_guardados.append(Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=o['cuenta'],
				fecha_indicativa=o['periodo'] or self.fecha_operacion,
				valor=o['monto']*self.direccion,
				detalle=o['detalle'],
			))
		if self.resultados:
			for o in self.cargas_guardadas:
				self.cobros_guardados.append(Operacion.objects.create(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento = self.documento,
					asiento=self.identifier,
					cuenta=o.cuenta,
					fecha_indicativa=o.fecha_indicativa,
					valor=-o.valor,
					detalle=o.detalle,
					vinculo=o,
				))						
			

	def hacer_cierre(self):
		""" Genera un movimiento más si el saldo de todas las operaciones hechas es != de 0"""
		operaciones = self.cargas_guardadas+self.cobros_guardados+self.cajas_guardadas+self.resultados_guardados
		saldo = sum([o.valor for o in operaciones])
		if saldo != 0:
			_ = Operacion.objects.create(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento = self.documento,
				asiento=self.identifier,
				cuenta=self.documento.destinatario,
				fecha_indicativa=self.fecha_operacion,
				valor=-saldo*self.direccion,
			)

	def create(self):

		self.hacer_cargas()

		self.hacer_cobros()
		
		self.hacer_cajas()

		self.hacer_resultados()

		self.hacer_cierre()

