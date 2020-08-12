from admincu.operative.models import Cobro
from django_filters.rest_framework import FilterSet, filters


class CobroPlataformaFilter(FilterSet):
    
    # plataforma__platform_code = django_filters.CharFilter(label="Apellido del corredor", lookup_expr="icontains")

    class Meta:
        model = Cobro
        fields = ['cliente', 'plataforma__platform_code']
