from adminsmart.operative.models import Operacion
from django_filters.rest_framework import FilterSet, DateFilter, CharFilter


class InformesFilter(FilterSet):

    start_date = DateFilter(field_name="fecha", lookup_expr="gte")
    end_date = DateFilter(field_name="fecha", lookup_expr="lte")
    # documento__receipt__receipt_type__description = CharFilter(field_name='documento__receipt__receipt_type__description')

    # cuenta__naturaleza__nombre = CharFilter(field_name='cuenta__naturaleza__nombre')
    

    class Meta:
        model = Operacion
        fields = {
            # 'cuenta': ['exact','in'],
            'documento__receipt__receipt_type__description': ['exact', 'in'],
            # 'cuenta__naturaleza__nombre': ['exact', 'in'],
            # 'cuenta__titulo': ['exact', 'in']
        }