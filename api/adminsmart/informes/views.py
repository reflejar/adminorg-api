from django.http import Http404
from datetime import datetime

from rest_framework.response import Response
from rest_framework import status
from django_afip.models import (
	DocumentType,
	ReceiptType,
)
from adminsmart.utils.generics import custom_viewsets
from adminsmart.operative.models import (
	Operacion
)
from .filter import InformesFilter

class InformesViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Unicamente se hacen peticiones GET
		Es la vista para recopilar la data para hacer reportes y analisis
	"""

	http_method_names = ['get']
	filterset_class = InformesFilter

	def get_queryset(self):
		try:
			datos = Operacion.objects.filter(
				comunidad=self.comunidad,
				documento__isnull=False
			).select_related(
				"cuenta", 
				"cuenta__perfil", # Para el nombre de la cuenta
				"cuenta__titulo", 
				"cuenta__naturaleza",
				"documento__receipt", 
				"documento__receipt__receipt_type", 
				"vinculo",
			).prefetch_related(
				"vinculos",
				"vinculos__cuenta",
				"vinculos__cuenta__naturaleza",
				"vinculo__vinculos",
				"vinculo__vinculos__cuenta",
				"vinculo__vinculos__cuenta__naturaleza",
			)
			self.filter = self.filterset_class(self.request.GET, queryset=datos)
			return self.filter.qs
		except:
			raise Http404

	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		end_date = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date()
		serializer_context['end_date'] = end_date
		return serializer_context

	def list(self, request):
		queryset = self.get_queryset()

		if "xls_all" in self.request.GET:
			# TODO: Hacer el xls y retornar
			return "xls"

		analisis_config = self.request.GET['analisis_config'] # JSON para el analisis

		# data = analisis(queryset, analisis_config)

		return Response(data)