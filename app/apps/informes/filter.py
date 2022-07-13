from apps.core.models import Operacion
from django_filters.rest_framework import FilterSet, DateFilter, CharFilter


class InformesFilter(FilterSet):

    start_date = DateFilter(label="Fecha desde", field_name="fecha", lookup_expr="gte")
    end_date = DateFilter(label="Fecha hasta", field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Operacion
        fields = []
