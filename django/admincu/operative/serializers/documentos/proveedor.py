from django.db import transaction

from .base import *

from admincu.operative.serializers.operaciones.proveedor import (
	DebitoModelSerializer,
	PagoModelSerializer,
	CajaModelSerializer,
	ACuentaModelSerializer,
	UtilizacionModelSerializer,
	ResultadoModelSerializer,
	RetencionModelSerializer,
)

from admincu.operative.CU.operaciones.proveedores import (
	debitos as operacionesDebitos,
	disminuciones as operacionesDisminuciones
)

debitos = ["1", "2", "6", "7", "63", "64", "11", "12", "51", "52"]
disminuciones = ["301", "3", "8", "13", "53"]
creador_operaciones = {}

for d in disminuciones:
	creador_operaciones.update({
		d: operacionesDisminuciones.CU
	})

for d in debitos:
	creador_operaciones.update({
		d: operacionesDebitos.CU
	})

class OrigenProveedorModelSerializer(DocumentoModelSerializer):
	'''Documento origen proveedor model serializer'''

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Incorporacion por TIPOS de documento
		if 'receipt_type' in self.context.keys():		
			self.sumas = {
				'debitos': 0,
				'pagos': 0, 
				'cajas': 0,
				'utilizaciones_saldos': 0,
				'retenciones': 0,
				'resultados': 0,
			}
			if self.context['receipt_type'].code in debitos: 
				self.fields['debitos'] = DebitoModelSerializer(context=self.context, read_only=False, many=True) # Equivalente al "creditos" de Clientes

			if self.context['receipt_type'].code in disminuciones:
				self.fields['pagos'] = PagoModelSerializer(context=self.context, read_only=False, many=True)
				if self.context['receipt_type'].code == "301":
					self.fields['cajas'] = CajaModelSerializer(context=self.context, read_only=False, many=True)
					self.fields['utilizaciones_saldos'] = UtilizacionModelSerializer(context=self.context, read_only=False, many=True)
					self.fields['retenciones'] = RetencionModelSerializer(context=self.context, read_only=False, many=True)
					self.fields['a_cuenta'] = ACuentaModelSerializer(context=self.context, read_only=True, many=True)
				else:	
					self.fields['resultados'] = ResultadoModelSerializer(context=self.context, read_only=False, many=True)
				

	def ejecutar_totales(self, data):
		"""
			Realiza los totales y los guarda en un dict
		"""
		for clave in self.sumas.keys():
			if clave in data.keys():
				self.sumas[clave] = sum([i['monto'] for i in data[clave]])

		self.suma_debe = self.sumas['pagos'] + self.sumas['debitos']
		self.suma_haber = self.sumas['cajas'] + self.sumas['utilizaciones_saldos'] + self.sumas['retenciones'] + self.sumas['resultados']
		

	def valid_totales(self, data):
		"""
			Validacion de total en Ordenes de Pago. 
			No se permite:
		"""
		error = False

		if self.context['receipt_type'].code in disminuciones:
			if self.suma_debe > self.suma_haber:
				raise serializers.ValidationError('El total de los debitos que intenta cancelar es mayor al total por formas de pago')
		else:
			if self.suma_debe < self.suma_haber:
				raise serializers.ValidationError('El total de las formas de pago es mayor al total de lo que desea cancelar')

		return True

	def valid_receipt_number(self, data):
		"""
			Validacion unicamente para proveedores para no cargar documentos != 301 con el mismo receipt_number
		"""
		receipt_type = self.context['receipt_type']
		destinatario = data['destinatario']
		receipt = data['receipt']

		receipts = OwnReceipt.objects.filter(
			receipt_type=receipt_type,
			point_of_sales=receipt['point_of_sales'],
			document_type=destinatario.perfil.tipo_documento,
			document_number=destinatario.perfil.numero_documento,
			receipt_number=receipt['receipt_number'],
		)
		if receipts:
			if self.instance:
				if self.instance.receipt in list(receipts):
					return data
			raise serializers.ValidationError({'receipt': {'receipt_number': 'El documento que desea ingresar ya existe en la base de datos'}})
		return data

	def valid_pagos(self, data):
		"""
			Validacion de pagos. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de los pagos juntos
			No se permite si:
				el pago no pertenece al destinatario
				existe un pago de capital posterior a la fecha_operacion recibida
				el "valor" colocado para el pago es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario = data['destinatario']
		fecha_operacion = data['fecha_operacion']
		pagos = data['pagos']
		for c in pagos:
			deuda = c['vinculo']
			if not deuda.cuenta == destinatario:
				raise serializers.ValidationError({'pagos': {deuda.id: "No es un deuda perteneciente al proveedor"}})
			# Esta validacion desconozco porque esta en PROVEEDORES. En clientes si, pero aqui aun no se. Por las dudas la deje
			pagos = deuda.pagos_capital()
			if pagos:
				if pagos.filter(fecha__gt=fecha_operacion):
					raise serializers.ValidationError({'pagos': {deuda.id: "La deuda posee un pago posterior"}})

			# Aqui se debe realizar dos validaciones != si se trata de una creacion o de una actualizacion
			if self.instance:
				if deuda.saldo(fecha=fecha_operacion) + self.instance.receipt.total_amount < c['monto']:
					raise serializers.ValidationError({'pagos': {deuda.id: "El valor colocado es mayor al saldo del deuda"}})
			else:
				if deuda.saldo(fecha=fecha_operacion) < c['monto']:
					raise serializers.ValidationError({'pagos': {deuda.id: "El valor colocado es mayor al saldo del deuda"}})
		return data

	def valid_utilizaciones(self, data):
		"""
			Validacion de las utilizaciones_saldos de saldos y cheques. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de las utilizaciones_saldos juntos
			No se permite si:
				no existen debitos
				la utilizacion no pertenece a un destinatario del grupo
				el "valor" colocado para la utilizacion es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario = data['destinatario']
		fecha_operacion = data['fecha_operacion']
		utilizaciones_saldos = data['utilizaciones_saldos']
		pagos = data['pagos'] if 'pagos' in data.keys() else None
		if not pagos and utilizaciones_saldos:
			raise serializers.ValidationError('No se pueden utilizar operaciones si no se pagan debitos')
		for u in utilizaciones_saldos:
			operacion = u['vinculo']
			if not operacion.cuenta == destinatario:
				raise serializers.ValidationError({'utilizaciones_saldos': {operacion.id: 'No es una operacion utilizable. No pertenece al proveedor'}})
			
			if abs(operacion.saldo(fecha_operacion)) < u['monto']:
				raise serializers.ValidationError({'utilizaciones_saldos': {operacion.id: 'El valor colocado es mayor al saldo de la utilizacion'}})
		return data

	def valid_debitos(self, data):
		"""
			Validacion la creacion de debitos. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de las utilizaciones_saldos juntos
			No se permite si:
				no existen
		"""
		
		debitos = data['debitos']
		if not debitos:
			raise serializers.ValidationError('Debe agregar debitos')
		return data

	def validate(self, data):
		"""
			Llama a las funciones necesarias para validar
		"""

		self.ejecutar_totales(data)

		if self.context['receipt_type'].code != "301":
			self.valid_receipt_number(data)

		if self.context['receipt_type'].code in debitos:
			validacion_debitos = self.valid_debitos(data)		
		
		if self.context['receipt_type'].code in disminuciones:
			validacion_totales = self.valid_totales(data)
			validacion_pagos = self.valid_pagos(data)
			if self.context['receipt_type'].code == "301":
				validacion_utilizaciones_saldos = self.valid_utilizaciones(data)


		return data

	def hacer_total(self, validated_data):
		"""
			Crea el total_amount
				Si existe el field pagos, entonces desde ahi
				Sino desde cajas
				Y sino desde Debitos
		"""

		if self.context['receipt_type'].code in disminuciones:
			return self.suma_haber
		else:
			return self.suma_debe

	@transaction.atomic
	def create(self, validated_data):
		validated_data['receipt']['total_amount'] = self.hacer_total(validated_data)
		documento = super().create(validated_data)
		operaciones = creador_operaciones[self.context['receipt_type'].code](documento, validated_data).create()
		if self.context['receipt_type'].code == "301":
			documento.hacer_pdf()
		return documento

	
	@transaction.atomic
	def update(self, instance, validated_data):
		"""
			Se actualizan los datos de cabecera del documento
			Se eliminan las operaciones anteriores y se crean nuevas
		"""

		instance.fecha_operacion = validated_data['fecha_operacion']
		instance.destinatario = validated_data['destinatario']
		instance.descripcion = validated_data['descripcion']
		instance.receipt.receipt_type = ReceiptType.objects.get(description=validated_data['receipt']['receipt_type'])
		instance.receipt.point_of_sales = validated_data['receipt']['point_of_sales']
		if self.context['receipt_type'].code != "301":
			instance.receipt.receipt_number = validated_data['receipt']['receipt_number']
		instance.receipt.issued_date = validated_data['receipt']['issued_date']
		instance.receipt.total_amount = self.hacer_total(validated_data)
		instance.receipt.save()
		instance.save()

		instance.eliminar_operaciones()
		operaciones = creador_operaciones[instance.receipt.receipt_type.code](instance, validated_data).create()
		if self.context['receipt_type'].code == "301":
			instance.hacer_pdf()
		return instance