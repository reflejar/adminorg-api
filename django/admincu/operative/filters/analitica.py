from admincu.users.models import Perfil
from admincu.operative.models import Operacion
from django_filters.rest_framework import FilterSet, filters, DateFilter
from django.db.models import Q


class AnaliticaFilter(FilterSet):

    start_date = DateFilter(field_name="fecha", lookup_expr="gte")
    end_date = DateFilter(field_name="fecha", lookup_expr="lte")

    class Meta:
        model = Operacion
        fields = {
            'cuenta': ['in'],
        }
