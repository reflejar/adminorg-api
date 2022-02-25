from datetime import date
from django_afip.models import (
	Receipt,
	ReceiptType
)
from django.db.models import Max
from rest_framework import serializers

from adminsmart.core.models import (
	Documento, 
	Operacion,
	Cuenta
)
from adminsmart.utils.generics.functions import *


class CU:
	'''Operacion de transferencias realizadas en tesoreria'''

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.cargas = validated_data['cargas']
		self.cajas = validated_data['cajas']
		self.utilizaciones_disponibilidades = validated_data['utilizaciones_disponibilidades']
		self.suma_debe = 0
		self.suma_haber = 0
		self.operaciones = []

	def hacer_cargas(self):
		""" Realiza las operaciones de entrada de dinero """
		for i in self.cargas:
			self.suma_debe += i['monto']
			operacion_debe_carga = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				fecha_indicativa=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_debe_carga)



	def hacer_cajas(self):
		""" Realiza las operaciones de caja """
		for i in self.cajas:
			self.suma_haber += i['monto']
			operacion_haber_caja = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				fecha_indicativa=self.fecha_operacion,
				asiento=self.identifier,
				fecha_vencimiento=i['fecha_vencimiento'],
				cuenta=i['cuenta'],
				valor=-i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_haber_caja)


	def hacer_utilizaciones_disponibilidades(self):
		""" Realiza las operaciones de utilizaciones_disponibilidades """
		for i in self.utilizaciones_disponibilidades:
			self.suma_haber += i['monto']
			operacion_haber_disponibilidad = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				fecha_indicativa=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=i['vinculo'].cuenta,
				valor=-i['monto'],
				detalle=i['detalle'],
				vinculo=i['vinculo'],
			)
			self.operaciones.append(operacion_haber_disponibilidad)

	def create(self):
		
		self.hacer_cargas()
		self.hacer_cajas()
		self.hacer_utilizaciones_disponibilidades()

		Operacion.objects.bulk_create(self.operaciones)
		return Operacion.objects.filter(asiento=self.identifier)
