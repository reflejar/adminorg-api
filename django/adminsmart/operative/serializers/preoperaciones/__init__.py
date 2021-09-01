# from .individual import *
# from .masivo import *
from django.db import transaction

from adminsmart.operative.models import PreOperacion
from adminsmart.operative.serializers.operaciones.cliente import CreditoModelSerializer


class PreOperacionesModelSerializer(CreditoModelSerializer):
	'''Operacion de saldo a favor de cliente, solo lectura'''

	def get_metodo(self, cuenta, naturaleza):
		
		try:
			return cuenta.metodos.get(naturaleza=naturaleza)
		except:
			return

	@transaction.atomic
	def create(self, validated_data):
		
		pre_operaciones = []

		if validated_data['concepto'].naturaleza == 'ingreso': #Esta importando cargas
			metodo_interes = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='interes')
			metodo_descuento = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='descuento') 
			pre_operacion_debe = PreOperacion.objects.create(
				comunidad=self.context['comunidad'],
				cuenta=validated_data['destinatario'],
				valor=validated_data['monto'],
				detalle=validated_data['detalle'],
				fecha_indicativa=validated_data['periodo'],
				fecha_gracia=validated_data['fecha_gracia'],
				fecha_vencimiento=validated_data['fecha_vencimiento'],
			)
			if metodo_interes:
				pre_operacion_debe.metodos.add(metodo_interes)
			if metodo_descuento:
				pre_operacion_debe.metodos.add(metodo_descuento)
			
			pre_operaciones.append(pre_operacion_debe)
			pre_operacion_haber = PreOperacion.objects.create(
				comunidad=self.context['comunidad'],
				cuenta=validated_data['concepto'],
				valor=-validated_data['monto'],
				detalle=validated_data['detalle'],
				cantidad=validated_data['cantidad'],
				vinculo=pre_operacion_debe,
				fecha_indicativa=validated_data['periodo'],
				)
			pre_operaciones.append(pre_operacion_haber)

		else: #Esta importando cobros (caja)

			pre_operacion_haber = PreOperacion.objects.create(
				comunidad=self.context['comunidad'],
				cuenta=validated_data['destinatario'],
				valor=-validated_data['monto'],
				detalle=validated_data['detalle'],
				cantidad=validated_data['cantidad'],
				
				fecha_indicativa=validated_data['periodo'],
			)
			pre_operaciones.append(pre_operacion_haber)
			
			 
			pre_operacion_debe = PreOperacion.objects.create(
				comunidad=self.context['comunidad'],
				cuenta=validated_data['concepto'],
				valor=validated_data['monto'],
				detalle=validated_data['detalle'],
				vinculo=pre_operacion_haber,
				fecha_indicativa=validated_data['periodo'],
				fecha_gracia=validated_data['fecha_gracia'],
				fecha_vencimiento=validated_data['fecha_vencimiento'],
			)
	
		
			pre_operaciones.append(pre_operacion_debe)
		return pre_operaciones

	@transaction.atomic
	def update(self, instance, validated_data):
		"""
			Se actualiza: Cuenta, Perfil y Domicilio.
			Se construye un cliente completo.
		"""
			
		# Actualizacion de Nombre
		instance.cuenta = validated_data['destinatario']
		instance.valor = validated_data['monto']
		instance.detalle = validated_data['detalle']
		instance.fecha_indicativa = validated_data['periodo']
		instance.fecha_gracia = validated_data['fecha_gracia']
		instance.fecha_vencimiento = validated_data['fecha_vencimiento']
		instance.save()

		instance_concepto = instance.vinculos.filter(cuenta__naturaleza__nombre="ingreso").first()
		instance_concepto.cuenta = validated_data['concepto']
		instance_concepto.valor = -validated_data['monto']
		instance_concepto.detalle = validated_data['detalle']
		instance_concepto.cantidad = validated_data['cantidad']
		instance_concepto.fecha_indicativa = validated_data['periodo']
		instance_concepto.save()

		return instance		