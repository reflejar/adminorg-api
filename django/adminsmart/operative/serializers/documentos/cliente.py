from django.db import transaction

from .base import *

from django.template.loader import render_to_string

from adminsmart.operative.serializers.operaciones.cliente import (
	CreditoModelSerializer,
	CobroModelSerializer,
	CajaModelSerializer,
	UtilizacionModelSerializer,
	ACuentaModelSerializer,
	ResultadoModelSerializer
)

from adminsmart.operative.CU.operaciones.clientes import (
	creditos as operacionesCreditos,
	disminuciones as operacionesDisminuciones
)
from adminsmart.taskapp.tasks import send_emails

creditos = ['11', '12', '51', '52']
disminuciones = ['13', '53', '54']

creador_operaciones = {
	'11': operacionesCreditos.CU,
	'12': operacionesCreditos.CU,
	'51': operacionesCreditos.CU,
	'52': operacionesCreditos.CU,
	'13': operacionesDisminuciones.CU,
	'53': operacionesDisminuciones.CU,
	'54': operacionesDisminuciones.CU,
}

class DestinoClienteModelSerializer(DocumentoModelSerializer):
	'''Documento con destino a cliente model serializer'''

		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# Incorporacion por TIPOS de documento
		if 'receipt_type' in self.context.keys():
			if self.context['receipt_type'].code in creditos:
				self.fields['creditos'] = CreditoModelSerializer(context=self.context, read_only=False, many=True)

			elif self.context['receipt_type'].code in disminuciones:
				self.fields['cobros'] = CobroModelSerializer(context=self.context, read_only=False, many=True)
				self.fields['a_cuenta'] = ACuentaModelSerializer(context=self.context, read_only=True, many=True)
				
				# Incorporacion para Recibo X
				if self.context['receipt_type'].code == '54':
					self.fields['condonacion'] = serializers.BooleanField(required=True)
					self.fields['cajas'] = CajaModelSerializer(context=self.context, read_only=False, many=True)
					self.fields['utilizaciones_saldos'] = UtilizacionModelSerializer(context=self.context, read_only=False, many=True)
					self.fields['utilizaciones_disponibilidades'] = UtilizacionModelSerializer(context=self.context, read_only=False, many=True)
				
				# Incorporacion para Nota de Credito
				else:
					self.fields['resultados'] = ResultadoModelSerializer(context=self.context, read_only=False, many=True)


	def valid_creditos(self, data):
		"""
			Validacion de creditos. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de los creditos juntos
			No se permite si:
				La cuenta destinatario dentro del credito no está vinculada con el destinatario del JSON general
		"""
		destinatario_documento = data['destinatario']
		data_creditos = data['creditos']
		grupo = destinatario_documento.grupo
		for c in data_creditos:
			if not c['destinatario'] in grupo:
				raise serializers.ValidationError({'creditos': 'destinatario id {}: no es un destinatario de credito posible.'.format(c['destinatario'].id)})
		return data

	def valid_cobros(self, data):
		"""
			Validacion de cobros. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de los creditos juntos
			No se permite si:
				el credito no pertenece a un destinatario del grupo
				existe un pago de capital posterior a la fecha_operacion recibida
				el "valor" colocado para el credito es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario_documento = data['destinatario']
		grupo = destinatario_documento.grupo
		fecha_operacion = data['fecha_operacion']
		cobros = data['cobros']
		condonacion = data['condonacion'] if self.context['receipt_type'].code == '54' else True
		for d in cobros:
			credito = d['vinculo']
			if not credito.cuenta in grupo:
				raise serializers.ValidationError({'cobros': {credito.id: "No es un credito perteneciente al cliente / socio"}})

			pagos = credito.pagos_capital()
			if pagos:
				if pagos.filter(fecha__gt=fecha_operacion, documento__fecha_anulacion__isnull=True):
					raise serializers.ValidationError({'cobros': {credito.id: "El credito posee un pago de capital posterior"}})

			if credito.saldo(fecha=fecha_operacion, condonacion=condonacion) < d['monto']:
				raise serializers.ValidationError({'cobros': {credito.id: "El valor colocado es mayor al saldo del credito"}})

		return data

	def valid_totales(self, data):
		"""
			Validacion de total en recibos. 
			No se permite si:
				la suma de los cobros es mayor a la suma de las cajas y las utilizaciones_saldos
		"""
		suma = 0 
		suma_cajas = sum([i['monto'] for i in data['cajas']]) 
		suma_utilizaciones_saldos = sum([i['monto'] for i in data['utilizaciones_saldos']]) 
		suma_utilizaciones_disponibilidades = sum([i['monto'] for i in data['utilizaciones_disponibilidades']]) 
		suma_cobros = sum([i['monto'] for i in data['cobros']]) 
		
		if suma_cobros > (suma_cajas + suma_utilizaciones_saldos + suma_utilizaciones_disponibilidades):
			raise serializers.ValidationError('El valor de los creditos cobrados es mayor al total por formas de cobro')

		return suma

	def valid_utilizaciones(self, data):
		"""
			Validacion de las utilizaciones_saldos y de utilizaciones_disponibilidades. 
			Solo se puede hacer en la validacion grupal para poder acceder a destinatario y destinatario de las utilizaciones_saldos juntos
			No se permite si:
				no existen cobros
				la utilizacion no pertenece al destinatario del documento
				el "valor" colocado para la utilizacion es mayor a su saldo a la "fecha_operacion" colocada
		"""
		destinatario_documento = data['destinatario']
		grupo = destinatario_documento.grupo
		fecha_operacion = data['fecha_operacion']
		utilizaciones_saldos = data['utilizaciones_saldos']
		if utilizaciones_saldos:
			cobros = data['cobros']
			if not cobros:
				raise serializers.ValidationError('No se pueden utilizar operaciones si no se pagan creditos')
			for u in utilizaciones_saldos:
				operacion = u['vinculo']
				if not operacion.cuenta in grupo:
					raise serializers.ValidationError({'utilizaciones_saldos': 'vinculo id {}: no es una operacion utilizable. No pertenece al cliente / socio'.format(operacion.id)})
				
				if abs(operacion.saldo(fecha_operacion)) < u['monto']:
					raise serializers.ValidationError({'utilizaciones_saldos': 'vinculo id {}: el valor colocado es mayor al saldo de la utilizacion'.format(operacion.id)})
		
		utilizaciones_disponibilidades = data['utilizaciones_disponibilidades']
		if utilizaciones_disponibilidades:
			for u in utilizaciones_disponibilidades:
				operacion = u['vinculo']
				if abs(operacion.saldo(fecha_operacion)) < u['monto']:
					raise serializers.ValidationError({'utilizaciones_disponibilidades': 'vinculo id {}: el valor colocado es mayor al saldo de la utilizacion'.format(operacion.id)})
		
		return data
		


	def valid_resultados(self, data):
		"""
			Validacion de total en notas de credito manuales. 
			No se permite si:
				la suma de los cobros es mayor a la suma de resultados
		"""
		suma = 0 
		suma_resultados = sum([i['monto'] for i in data['resultados']]) 
		suma_cobros = sum([i['monto'] for i in data['cobros']]) 
		
		if suma_cobros > suma_resultados:
			raise serializers.ValidationError('El valor de los creditos cobrados es mayor al total por resultados')

		return suma

	def validate(self, data):
		"""
			Llama a las funciones necesarias para validar
		"""

		if self.context['receipt_type'].code in creditos:
			validacion_creditos = self.valid_creditos(data)

		elif self.context['receipt_type'].code in disminuciones:
			validacion_cobros = self.valid_cobros(data)

			if self.context['receipt_type'].code == '54':
				validacion_utilizaciones = self.valid_utilizaciones(data)
				validacion_totales = self.valid_totales(data)

			else:
				validacion_resultados = self.valid_resultados(data)
		
		return data
		

	def hacer_total(self, validated_data):
		"""
			Crea el total_amount
				Si existe el field creditos, entonces desde ahi
				Sino desde cajas
				Y sino desde Debitos
		"""

		if self.context['receipt_type'].code in creditos:
			return sum([i['monto'] for i in validated_data['creditos']])

		elif self.context['receipt_type'].code == '54':
			return sum([i['monto'] for i in validated_data['cajas']])			

		elif self.context['receipt_type'].code in disminuciones:
			return sum([i['monto'] for i in validated_data['resultados']])	
		
		else:
			return 0.00

	@transaction.atomic
	def create(self, validated_data):
		validated_data['receipt']['total_amount'] = self.hacer_total(validated_data)
		documento = super().create(validated_data)
		operaciones = creador_operaciones[self.context['receipt_type'].code](documento, validated_data).create()
		documentos = set([o.documento for o in operaciones])
		for d in documentos:
			documento.hacer_pdf()

		self.send_email(documento)		
		return documento

	def send_email(self, documento):
		if documento.comunidad.mails:
			from_email = "{} <info@admin-smart.com>".format(documento.comunidad.nombre)
			destinations = documento.destinatario.perfil.get_emails_destinatarios()
			html_string = render_to_string('emails/documentos/index.html', {"documento": documento})
			subject = "Nuevo Comprobante" 
			file_paths = [documento.pdf.path]
			send_emails.delay(
				from_email=from_email, 
				destinations=destinations, 
				subject=subject, 
				html_string=html_string, 
				file_paths=file_paths
			)
