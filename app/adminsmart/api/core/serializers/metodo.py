from rest_framework import serializers
from adminsmart.apps.core.models import (
	Metodo,
	Naturaleza
)

apropiadores = ['ingreso', 'proveedor']

class MetodoModelSerializer(serializers.ModelSerializer):
	'''Metodo model serializer'''

	class Meta:
		model = Metodo

		fields = (
			'id',
			'nombre',
			'tipo',
			'plazo',
			'monto',
		)    

	def __init__(self, *args, **kwargs):
		super(MetodoModelSerializer, self).__init__(*args, **kwargs)

		# Incorporacion de Nombre
		if self.context['naturaleza'] in ['interes']:
			self.fields['reconocimiento'] = serializers.IntegerField()
			self.fields['base_calculo'] = serializers.IntegerField()


	def validate(self, data):
		'''
		Verifica que el id del metodo exista en la comunidad, y que sea de la naturaleza que corresponde.
		Validacion realizada solo a nivel de serializer para evitar la utilizacion de unique together en el models.
		Utiliza la comunidad que siempre es recibida en el context del serializer.
			'''
		if self.context['naturaleza'] in apropiadores:
			if self.context['naturaleza'] == 'proveedor':
				naturaleza_metodos = ['retencion']
			if self.context['naturaleza'] == 'ingreso':
				naturaleza_metodos = ['interes', 'descuento']
			try:
				metodo = Metodo.objects.get(id=data['id'])
				if not metodo.comunidad == self.context['comunidad'] or not metodo.naturaleza in naturaleza_metodos:
					raise serializers.ValidationError('El metodo seleccionado no es una opcion valida')
			except:
				raise serializers.ValidationError('El metodo seleccionado no es una opcion valida')
		return data

	
	def create(self, validate_data):
		if not self.context['naturaleza'] in ['proveedor', 'ingreso']:
			metodo = Metodo.objects.create(
				**validate_data,
				comunidad = self.context['comunidad'],
				naturaleza = self.context['naturaleza']
			)
			return metodo
