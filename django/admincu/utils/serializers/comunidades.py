from rest_framework import serializers

from admincu.utils.models import Comunidad


class ComunidadModelSerializer(serializers.ModelSerializer):
    '''Comunidad model serializer'''

    tipo = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='nombre'
     )
    class Meta:
        model = Comunidad
        fields = ('nombre', 'tipo',)