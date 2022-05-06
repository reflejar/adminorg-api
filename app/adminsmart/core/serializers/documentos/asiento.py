from django.db import transaction

from .base import *

from adminsmart.core.serializers.operaciones.asiento import (
	LineaModelSerializer,
)

from adminsmart.core.CU.operaciones.contabilidad import CU


class AsientoModelSerializer(DocumentoModelSerializer):
	'''
		Documento interno serializer.
		Hoy: Transferencia entre cajas y Asientos
	'''
	suma_debe = 0
	suma_haber = 0


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['debe'] = LineaModelSerializer(context=self.context, read_only=False, many=True)
		self.fields['haber'] = LineaModelSerializer(context=self.context, read_only=False, many=True)


	def valid_totales(self, data):
		"""
			Validacion de total en documentos internos. 
			No se permite si:
				la suma del debe y el haber no son iguales
		"""
		self.suma_debe = sum([i['monto'] for i in data['debe']]) 
		self.suma_haber = sum([i['monto'] for i in data['haber']]) 

		if self.suma_debe != self.suma_haber:
			raise serializers.ValidationError('Los valores no cierran.')

		return data

	def validate(self, data):
		"""
			Llama a las funciones necesarias para validar
		"""
		self.valid_totales(data)
		return data


	@transaction.atomic
	def create(self, validated_data):
		validated_data['receipt']['total_amount'] = self.suma_debe
		documento = super().create(validated_data)
		operaciones = CU(documento, validated_data).create()
		return documento

	@transaction.atomic
	def update(self, instance, validated_data):
		"""
			Se actualizan los datos de cabecera del documento
			Se eliminan las operaciones anteriores y se crean nuevas
		"""

		instance.fecha_operacion = validated_data['fecha_operacion']
		instance.descripcion = validated_data['descripcion']
		instance.receipt.issued_date = validated_data['receipt']['issued_date']
		instance.receipt.total_amount = self.suma_debe
		instance.receipt.point_of_sales = validated_data['receipt']['point_of_sales']

		instance.eliminar_operaciones()
		operaciones = CU(instance, validated_data).create()
		return instance