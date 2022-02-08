from adminsmart.operative.models import Operacion
from django_filters.rest_framework import FilterSet, DateFilter, CharFilter


class InformesFilter(FilterSet):

    start_date = DateFilter(field_name="fecha", lookup_expr="gte")
    end_date = DateFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Operacion
        fields = []
