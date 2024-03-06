from datetime import date
from django_afip.models import ReceiptType
from django.db.models import Max
from rest_framework import serializers

from apps.core.models import (
	Documento, 
	Operacion,
	Cuenta,
	OwnReceipt
)
from apps.utils.generics.functions import *


class CU:
	'''Operacion de pagos de deudas realizadas por proveedores'''

	notas_credito = ["3", "8", "13", "53"]
	op = ['301']

	def __init__(self, documento, validated_data):
		self.documento = documento
		self.receipt = documento.receipt
		self.comunidad = documento.comunidad
		self.identifier = randomIdentifier(Operacion, 'asiento')
		self.fecha_operacion = documento.fecha_operacion
		self.pagos = validated_data['pagos']
		if self.receipt.receipt_type.code in self.op:
			self.cajas = validated_data['cajas']
			self.utilizaciones_saldos = validated_data['utilizaciones_saldos']
		elif self.receipt.receipt_type.code in self.notas_credito:
			self.resultados = validated_data['resultados']

		self.suma_debe = 0
		self.suma_haber = 0
		self.operaciones = []

	def hacer_pagos(self):
		""" Realiza las operaciones de cobros de pagos """
		for i in self.pagos:
			self.suma_debe += i['monto']
			operacion_debe_pago = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				fecha_indicativa=self.fecha_operacion,
				cuenta=i['vinculo'].cuenta,
				valor=i['monto'],
				detalle=i['detalle'],
				vinculo=i['vinculo'],
			)
			self.operaciones.append(operacion_debe_pago)



	def hacer_cajas(self):
		""" Realiza las operaciones de caja """
		for i in self.cajas:
			self.suma_haber += i['monto']
			operacion_haber_caja = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				fecha_vencimiento=i['fecha_vencimiento'],
				fecha_indicativa=self.fecha_operacion,
				cuenta=i['cuenta'],
				valor=-i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_haber_caja)


	def hacer_utilizaciones_saldos(self):
		""" Realiza las operaciones de utilizaciones_saldos de saldos o cheques """
		for i in self.utilizaciones_saldos:
			self.suma_haber += i['monto']
			operacion_haber_saldo = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=i['vinculo'].cuenta,
				fecha_indicativa=self.fecha_operacion,
				valor=-i['monto'],
				detalle=i['detalle'],
				vinculo=i['vinculo'],
			)
			self.operaciones.append(operacion_haber_saldo)


	def hacer_saldo_a_favor(self):
		""" Realiza la operacion de saldo a favor """
		if self.suma_haber > self.suma_debe:
			operacion_debe_saldo = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				fecha_indicativa=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				cuenta=self.documento.destinatario,
				valor=self.suma_haber - self.suma_debe,
				detalle="Saldo a favor",
			)
			self.operaciones.append(operacion_debe_saldo)


	def hacer_resultados(self):
		""" Realiza las operaciones de la contraparte de los debitos perdonados en las Notas de Credito C manuales """
		for i in self.resultados:
			self.suma_haber += i['monto']
			operacion_debe_resultado = Operacion(
				comunidad=self.comunidad,
				fecha=self.fecha_operacion,
				documento=self.documento,
				asiento=self.identifier,
				fecha_indicativa=self.fecha_operacion,
				cuenta=i['cuenta'],
				valor=-i['monto'],
				detalle=i['detalle'],
			)
			self.operaciones.append(operacion_debe_resultado)


	def create(self):
		
		self.hacer_pagos()
		if self.receipt.receipt_type.code in self.op:
			self.hacer_cajas()
			self.hacer_utilizaciones_saldos()
			self.hacer_saldo_a_favor()

		elif self.receipt.receipt_type.code in self.notas_credito:
			self.hacer_resultados()

		Operacion.objects.bulk_create(self.operaciones)
		return Operacion.objects.filter(asiento=self.identifier)
