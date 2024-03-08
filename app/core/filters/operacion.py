from users.models import Perfil
from core.models import Operacion
from django_filters.rest_framework import FilterSet, filters


class OperacionFilter(FilterSet):

    fecha = filters.DateRangeFilter(label="Fecha", lookup_expr="icontains")
    documento = filters.NumberFilter(label="Documento", lookup_expr="exact")

    class Meta:
        model = Operacion
        fields = []
