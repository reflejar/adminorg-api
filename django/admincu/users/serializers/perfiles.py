from rest_framework import serializers
from django_afip.models import DocumentType

from admincu.utils.serializers import DomicilioModelSerializer
from admincu.users.models import Perfil


class PerfilModelSerializer(serializers.ModelSerializer):
	'''Perfil model serializer'''
	
	domicilio = DomicilioModelSerializer(read_only=False)
	tipo_documento = serializers.ChoiceField(choices=list(DocumentType.objects.all().values_list('description', flat=True)))
	cuenta = serializers.SerializerMethodField()

	class Meta:
		model = Perfil
		fields = (
			'nombre',
			'apellido',
			'razon_social',
			'tipo_documento',
			'numero_documento',
			'fecha_nacimiento',
			'es_extranjero',
			'mail',
			'telefono',
			'domicilio',
			'cuenta'
		)

	def get_cuenta(self, obj):
		cuenta = obj.cuenta_set.first()
		if cuenta:
			return cuenta.id
		return 