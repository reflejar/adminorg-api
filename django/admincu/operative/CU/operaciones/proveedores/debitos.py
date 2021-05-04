from datetime import date
from django_afip.models import (
	Receipt,
	ReceiptType
)
from django.db.models import Max
from rest_framework import serializers

from admincu.operative.models import (
	Documento, 
	Operacion,
	Cuenta
)
from admincu.utils.generics.functions import *


class CU:
	'''Operacion de debitos realizada con proveedores'''

	def __init__(self, documento, validated_data):
		# super().__init__(documento, validated_data)
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.debitos = validated_data['debitos']
		self.suma_debe = 0
		self.operaciones = []		



	def hacer_debitos(self):
		for i in self.debitos:
			self.suma_debe += i['monto']
			operacion_debe_debito = Operacion(
				comunidad=self.comunidad,
				documento = self.documento,
				asiento=self.identifier,
				cantidad=i['cantidad'],
				cuenta=i['cuenta'],
				valor=i['monto'],
				detalle=i['detalle'],
				fecha=self.documento.fecha_operacion,
				fecha_indicativa=self.fecha_operacion,
				fecha_vencimiento=i['fecha_vencimiento'],
			)
			self.operaciones.append(operacion_debe_debito)

	def hacer_deuda(self):
		if self.suma_debe:
			operacion_haber_deuda = Operacion(
					comunidad=self.comunidad,
					fecha=self.fecha_operacion,
					documento=self.documento,
					asiento=self.identifier,
					cuenta=self.documento.destinatario,
					fecha_indicativa=self.fecha_operacion,
					valor=-self.suma_debe,
					detalle=self.documento.descripcion,
				)		
			self.operaciones.append(operacion_haber_deuda)



	def create(self):

		self.hacer_debitos()
		self.hacer_deuda()

		Operacion.objects.bulk_create(self.operaciones)
		return Operacion.objects.filter(asiento=self.identifier)