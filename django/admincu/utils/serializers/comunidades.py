from rest_framework import serializers

from admincu.utils.models import Comunidad


class ComunidadModelSerializer(serializers.ModelSerializer):
	'''Comunidad model serializer'''

	tipo = serializers.SlugRelatedField(
		many=False,
		read_only=True,
		slug_field='nombre'
	)
	afip = serializers.SerializerMethodField()
	
	class Meta:
		model = Comunidad
		fields = ('nombre', 'tipo', 'afip')


	def get_afip(self, obj):
		if obj.contribuyente:
			return not obj.contribuyente.is_sandboxed
		return False