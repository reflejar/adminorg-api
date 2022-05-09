import json
import pandas as pd
from django.http import Http404
from datetime import datetime
from django.http import HttpResponse
from io import BytesIO

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from adminsmart.apps.utils.generics import custom_viewsets
from adminsmart.apps.core.models import (
	Operacion,
	Cuenta
)
from adminsmart.apps.informes.filter import InformesFilter
from adminsmart.apps.informes.analisis import OperacionAnalisis

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

	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		end_date = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date()
		serializer_context['end_date'] = end_date
		return serializer_context


	def get_nombres(self):
		cuentas = Cuenta.objects.filter(
					comunidad=self.comunidad, 
					).select_related(
						"naturaleza",
					).prefetch_related(
						"vinculo2",
					)
		nombres = [
			{
				'CUENTA_ID': c.id, 
				'NATURALEZA': c.naturaleza.nombre,
				'NOMBRE': str(c) if c.naturaleza.nombre != "dominio" else str(c.inquilino())
			} for c in cuentas
		]		
		return nombres

	def list(self, request):
		queryset = self.get_queryset()
		analisis_config = eval(request.GET['analisis'])
		analisis = OperacionAnalisis(
				queryset=queryset, 
				nombres=self.get_nombres(), 
				analisis_config=analisis_config
			)
		df_json = analisis.get_df().to_json(orient='split')
		return Response(json.loads(df_json))

	@action(detail=False, methods=['get'])
	def xlsx(self, request):
		queryset = self.get_queryset()
		analisis_config = eval(request.GET['analisis'])
		analisis = OperacionAnalisis(
				queryset=queryset, 
				nombres=self.get_nombres(), 
				analisis_config=analisis_config
			)
		df = analisis.get_df(raw_data=True)
		with BytesIO() as b:
			# Use the StringIO object as the filehandle.
			writer = pd.ExcelWriter(b, engine='xlsxwriter')
			df.to_excel(writer, sheet_name='Informe')
			writer.save()
			filename = 'informe'
			content_type = 'application/vnd.ms-excel'
			response = HttpResponse(b.getvalue(), content_type=content_type)
			response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
			return response			