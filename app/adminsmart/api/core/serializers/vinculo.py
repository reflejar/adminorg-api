from rest_framework import serializers
from adminsmart.apps.core.models import (
	DefinicionVinculo,
	Taxon
)


class VinculoModelSerializer(serializers.ModelSerializer):
	'''Cuenta model serializer'''


	def __init__(self, *args, **kwrgs):
		super().__init__(*args, **kwargs)
		definicion = serializers.ChoiceField(required=True, choices=list(Taxon.objects.filter(naturaleza__nombre='dominio').values_list('nombre', flat=True)))

	class Meta:
		model = DefinicionVinculo

		fields = (
			'definicion',
			'cuenta_vinculada',
		)
