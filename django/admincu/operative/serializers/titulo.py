from rest_framework import serializers
from admincu.operative.models import (
	Cuenta,
	Titulo,
)

class CuentaModelSerializer(serializers.ModelSerializer):
	"""
		Serializer particular de Cuenta para Contabilidad
	"""

	nombre = serializers.SerializerMethodField()
	
	class Meta:
		model = Cuenta

		fields = (
			'id',
			'nombre'
		)
	
	def get_nombre(self, obj):

		return str(obj)


class TituloModelSerializer(serializers.ModelSerializer):
	'''Titulo model serializer'''

	# cuentas = serializers.SerializerMethodField()


	class Meta:
		model = Titulo

		fields = (
			'id',
			'nombre',
			'numero',
		)    

	def __init__(self, *args, **kwargs):
		super(TituloModelSerializer, self).__init__(*args, **kwargs)
		self.fields['supertitulo'] = serializers.PrimaryKeyRelatedField(queryset=Titulo.objects.filter(comunidad=self.context['comunidad']), allow_null=True)
		self.fields['cuentas'] = CuentaModelSerializer(read_only=True, many=True)
		


	def validate_nombre(self, nombre):
		"""
			No puede haber titulos con el mismo nombre 
		"""

		query = Titulo.objects.filter(
				comunidad=self.context['comunidad'], 
				nombre=nombre
			)

		if query:
			if self.context['request'].method == 'POST' or not self.instance in query:
				raise serializers.ValidationError('Ya existe un titulo con el nombre solicitado')

		return nombre

	def validate_numero(self, numero):
		"""
			No puede haber titulos con el mismo numero 
		"""

		query = Titulo.objects.filter(
				comunidad=self.context['comunidad'], 
				numero=numero
			)

		if query:
			if self.context['request'].method == 'POST' or not self.instance in query:
				raise serializers.ValidationError('Ya existe un titulo con el numero solicitado')
			
		return numero


	def validate_supertitulo(self, supertitulo):
		"""
			No puede colocar como supertitulo a un titulo que ya tiene cuentas asociadas 
		"""

		query = supertitulo.cuenta_set.all()

		if query:
			raise serializers.ValidationError('No se puede seleccionar un titulo que posee cuentas asociadas')
			
		return supertitulo


	def create(self, validate_data):
		titulo = Titulo.objects.create(
			**validate_data,
			comunidad = self.context['comunidad'],
		)
		return titulo
