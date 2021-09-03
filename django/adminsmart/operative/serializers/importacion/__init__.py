from django.db import transaction
from django.db.models import fields

from rest_framework import serializers

from adminsmart.operative.models import (
	PreOperacion,
	Cuenta
	) 


class ImportacionModelSerializer(serializers.ModelSerializer):
	'''Serializer de PreOperaciones'''

	class Meta:
		model = PreOperacion
		fields = (
			'id',
			'cantidad',
			'fecha_vencimiento',
			'fecha_gracia',
			'detalle',
			'descripcion',
		)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = PreOperacion()._meta
		self.fields['periodo'] = serializers.ModelField(model_field=fields.get_field("fecha_indicativa"))
		self.fields['monto'] = serializers.DecimalField(decimal_places=2, max_digits=15, min_value=0.01)
		self.fields['destinatario'] = serializers.PrimaryKeyRelatedField(
			queryset=Cuenta.objects.filter(
					comunidad=self.context['comunidad'], 
					naturaleza__nombre__in=['cliente', 'dominio']
				), 
			allow_null=False
		)
		self.fields['concepto'] = serializers.PrimaryKeyRelatedField(
			queryset=Cuenta.objects.filter(
					comunidad=self.context['comunidad'], 
					naturaleza__nombre__in=["ingreso", "caja"]
				), 
			allow_null=False
		)
		

		


	@classmethod
	def get_metodo(cls, cuenta, naturaleza):
		try:
			return cuenta.metodos.get(naturaleza=naturaleza)
		except:
			return

	@transaction.atomic
	def create(self, validated_data):
    		
		preoperacion = PreOperacion.objects.create(
			comunidad=self.context['comunidad'],
			cuenta=validated_data['destinatario'],
			valor=validated_data['monto'],
			detalle=validated_data['detalle'],
			fecha_indicativa=validated_data['periodo'],
			fecha_gracia=validated_data['fecha_gracia'],
			fecha_vencimiento=validated_data['fecha_vencimiento'],
		)

		metodo_interes = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='interes')
		metodo_descuento = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='descuento')

		if metodo_interes:
			preoperacion.metodos.add(metodo_interes)
		if metodo_descuento:
			preoperacion.metodos.add(metodo_descuento)
		
		return preoperacion


	# @transaction.atomic
	# def create(self, validated_data):
		
	# 	pre_operaciones = []

	# 	if validated_data['concepto'].naturaleza == 'ingreso': #Esta importando cargas
	# 		metodo_interes = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='interes')
	# 		metodo_descuento = self.get_metodo(cuenta=validated_data['concepto'], naturaleza='descuento') 
	# 		pre_operacion_debe = PreOperacion.objects.create(
	# 			comunidad=self.context['comunidad'],
	# 			cuenta=validated_data['destinatario'],
	# 			valor=validated_data['monto'],
	# 			detalle=validated_data['detalle'],
	# 			fecha_indicativa=validated_data['periodo'],
	# 			fecha_gracia=validated_data['fecha_gracia'],
	# 			fecha_vencimiento=validated_data['fecha_vencimiento'],
	# 		)
	# 		if metodo_interes:
	# 			pre_operacion_debe.metodos.add(metodo_interes)
	# 		if metodo_descuento:
	# 			pre_operacion_debe.metodos.add(metodo_descuento)
			
	# 		pre_operaciones.append(pre_operacion_debe)
	# 		pre_operacion_haber = PreOperacion.objects.create(
	# 			comunidad=self.context['comunidad'],
	# 			cuenta=validated_data['concepto'],
	# 			valor=-validated_data['monto'],
	# 			detalle=validated_data['detalle'],
	# 			cantidad=validated_data['cantidad'],
	# 			vinculo=pre_operacion_debe,
	# 			fecha_indicativa=validated_data['periodo'],
	# 			)
	# 		pre_operaciones.append(pre_operacion_haber)

	# 	else: #Esta importando cobros (caja)

	# 		pre_operacion_haber = PreOperacion.objects.create(
	# 			comunidad=self.context['comunidad'],
	# 			cuenta=validated_data['destinatario'],
	# 			valor=-validated_data['monto'],
	# 			detalle=validated_data['detalle'],
	# 			cantidad=validated_data['cantidad'],
				
	# 			fecha_indicativa=validated_data['periodo'],
	# 		)
	# 		pre_operaciones.append(pre_operacion_haber)
			
			 
	# 		pre_operacion_debe = PreOperacion.objects.create(
	# 			comunidad=self.context['comunidad'],
	# 			cuenta=validated_data['concepto'],
	# 			valor=validated_data['monto'],
	# 			detalle=validated_data['detalle'],
	# 			vinculo=pre_operacion_haber,
	# 			fecha_indicativa=validated_data['periodo'],
	# 			fecha_gracia=validated_data['fecha_gracia'],
	# 			fecha_vencimiento=validated_data['fecha_vencimiento'],
	# 		)
	
		
	# 		pre_operaciones.append(pre_operacion_debe)
	# 	return pre_operaciones

	# @transaction.atomic
	# def update(self, instance, validated_data):
	# 	"""
	# 		Se actualiza: Cuenta, Perfil y Domicilio.
	# 		Se construye un cliente completo.
	# 	"""
			
	# 	# Actualizacion de Nombre
	# 	instance.cuenta = validated_data['destinatario']
	# 	instance.valor = validated_data['monto']
	# 	instance.detalle = validated_data['detalle']
	# 	instance.fecha_indicativa = validated_data['periodo']
	# 	instance.fecha_gracia = validated_data['fecha_gracia']
	# 	instance.fecha_vencimiento = validated_data['fecha_vencimiento']
	# 	instance.save()

	# 	instance_concepto = instance.vinculos.filter(cuenta__naturaleza__nombre="ingreso").first()
	# 	instance_concepto.cuenta = validated_data['concepto']
	# 	instance_concepto.valor = -validated_data['monto']
	# 	instance_concepto.detalle = validated_data['detalle']
	# 	instance_concepto.cantidad = validated_data['cantidad']
	# 	instance_concepto.fecha_indicativa = validated_data['periodo']
	# 	instance_concepto.save()

	# 	return instance		

	@transaction.atomic
	def update(self, instance, validated_data):

		instance.cuenta = validated_data['destinatario']
		instance.valor = validated_data['monto']
		instance.detalle = validated_data['detalle']
		instance.fecha_indicativa = validated_data['periodo']
		instance.fecha_gracia = validated_data['fecha_gracia']
		instance.fecha_vencimiento = validated_data['fecha_vencimiento']
		instance.save()
	
		return instance





















































