from rest_framework import serializers
from django_afip.models import PointOfSales


class PuntoModelSerializer(serializers.ModelSerializer):
	'''Punto model serializer'''

	class Meta:
		model = PointOfSales

		fields = (
			'id',
			'number',
		)    


	def create(self, validate_data):
		punto = PointOfSales.objects.none()
		return punto
