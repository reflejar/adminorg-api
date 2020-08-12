from admincu.operative.models import Documento
from django_filters.rest_framework import FilterSet, filters


class DocumentoFilter(FilterSet):

    receipt__issued_date_from = filters.DateFilter(field_name="receipt__issued_date", lookup_expr='gte')
    receipt__issued_date_to = filters.DateFilter(field_name="receipt__issued_date", lookup_expr='lte')
    receipt__receipt_type__description = filters.CharFilter(field_name="receipt__receipt_type__description")

    class Meta:
        model = Documento
        fields = [
            'receipt__point_of_sales__number',
            'receipt__receipt_number',
        ]
