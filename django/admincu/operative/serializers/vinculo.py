from rest_framework import serializers
from admincu.operative.models import (
	DefinicionVinculo,
	Taxon
)


class VinculoModelSerializer(serializers.ModelSerializer):
	'''Cuenta model serializer'''

	#definicion = serializers.ChoiceField(required=True, choices=list(Taxon.objects.filter(naturaleza__nombre='dominio').values_list('nombre', flat=True)))

	class Meta:
		model = DefinicionVinculo

		fields = (
			'definicion',
			'cuenta_vinculada',
		)
