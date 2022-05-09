from django.db import transaction

from adminsmart.apps.core.CU.operaciones.tesoreria import CU

from adminsmart.api.core.serializers.operaciones.caja import (
	CargaModelSerializer,
	CajaModelSerializer,
	UtilizacionModelSerializer
)

from .base import *

class TesoroModelSerializer(DocumentoModelSerializer):
	'''
		Documento interno serializer.
		Hoy: Transferencia entre cajas
	'''

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if 'receipt_type' in self.context.keys():		
			self.sumas = {
				'cargas': 0,
				'cajas': 0,
				'utilizaciones_disponibilidades': 0
			}
			self.fields['cargas'] = CargaModelSerializer(context=self.context, read_only=False, many=True)
			self.fields['cajas'] = CajaModelSerializer(context=self.context, read_only=False, many=True)
			self.fields['utilizaciones_disponibilidades'] = UtilizacionModelSerializer(context=self.context, read_only=False, many=True)

	def ejecutar_totales(self, data):
		"""
			Realiza los totales y los guarda en un dict
		"""
		for clave in self.sumas.keys():
			if clave in data.keys():
				self.sumas[clave] = sum([i['monto'] for i in data[clave]])

		self.suma_debe = self.sumas['cargas']
		self.suma_haber = self.sumas['cajas'] + self.sumas['utilizaciones_disponibilidades']


	def valid_totales(self, data):
		"""
			Validacion de total en Ordenes de Pago. 
			No se permite:
		"""
		if self.suma_debe != self.suma_haber:
			raise serializers.ValidationError('El total de las cargas debe ser igual al total de las descargas')

	def validate_utilizaciones_disponibilidades(self, utilizaciones_disponibilidades):
		"""
			No puede utilizarse una disponibilidad que haya sido creada por una transferencia
		"""

		for ud in utilizaciones_disponibilidades:

			if ud['vinculo'].documento.receipt.receipt_type.code == "303":
				raise serializers.ValidationError('No se puede utilizar una disponibilidad creada desde una transferencia')
		return utilizaciones_disponibilidades


	def validate(self, data):
		"""
			Llama a las funciones necesarias para validar
		"""

		self.ejecutar_totales(data)

		self.valid_totales(data)


		return data		

	@transaction.atomic
	def create(self, validated_data):
		validated_data['receipt']['total_amount'] = self.suma_debe
		documento = super().create(validated_data)
		operaciones = CU(documento, validated_data).create()
		documento.hacer_pdf()
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
		instance.hacer_pdf()
		return instance