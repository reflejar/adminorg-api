import tempfile
import os
from django.http import Http404
from datetime import datetime
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from adminsmart.utils.generics import custom_viewsets
from adminsmart.core.models import (
	Operacion,
	Cuenta
)
from .filter import InformesFilter
from .analisis import OperacionAnalisis

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
		return Response(analisis.get_json())

	@action(detail=False, methods=['get'])
	def xlsx(self, request):
		queryset = self.get_queryset()
		analisis_config = eval(request.GET['analisis'])
		nombres = self.get_nombres()
		nombres.append({
				'CUENTA_ID': 0, 
				'NATURALEZA': "",
				'NOMBRE': "-"
			})
		analisis = OperacionAnalisis(
				queryset=queryset, 
				nombres=nombres, 
				analisis_config=analisis_config
			)
		data, filename = analisis.get_excel()
		response = HttpResponse(data, content_type="application/vnd.ms-excel")
		response['Content-Disposition'] = 'inline; filename=' + os.path.basename(filename)
		return response
