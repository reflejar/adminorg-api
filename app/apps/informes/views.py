import json
import pandas as pd
from django.http import Http404
from datetime import datetime
from django.http import HttpResponse
from io import BytesIO

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.utils.generics import custom_viewsets
from apps.core.models import (
	Operacion,
	Cuenta
)
from apps.informes.filter import InformesFilter
from apps.informes.analisis import OperacionAnalisis

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
				#documento__isnull=False
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


	def list(self, request):
		queryset = self.get_queryset()
		analisis_config = eval(request.GET['analisis'])

		analisis = OperacionAnalisis(
				queryset=queryset, 
				analisis_config=analisis_config
			)
		df_json = analisis.get_df().to_json(orient='records')
		return Response(json.loads(df_json))