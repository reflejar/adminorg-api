from adminsmart.apps.core.models import Documento
from django_afip.models import ReceiptType
from django_filters.rest_framework import FilterSet, filters

try:
	tipos = list(ReceiptType.objects.all().values_list('description', flat=True))
	TIPO_CHOICES = [[t,t] for t in tipos]
except:
	TIPO_CHOICES = []



class DocumentoFilter(FilterSet):

	receipt__issued_date_from = filters.DateFilter(
			label="Fecha desde",
			field_name="receipt__issued_date", 
			lookup_expr='gte'
		)
	receipt__issued_date_to = filters.DateFilter(
			label="Fecha hasta",
			field_name="receipt__issued_date", 
			lookup_expr='lte'
		)
	receipt__receipt_type__description = filters.ModelMultipleChoiceFilter(
			# choices=TIPO_CHOICES,
			label="Tipo de cbte",
			lookup_expr='in',
			field_name="receipt__receipt_type__description",
			queryset=ReceiptType.objects.all()
		)
	receipt__point_of_sales = filters.CharFilter(
			label="Punto Vta.",
			field_name="receipt__point_of_sales"
		)        
	receipt__receipt_number = filters.CharFilter(
			label="Número",
			field_name="receipt__receipt_number"
		)               

	class Meta:
		model = Documento
		fields = []
