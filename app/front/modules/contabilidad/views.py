import pandas as pd
from io import BytesIO

from django.views import generic

from django.http import (
	Http404,
	HttpResponse
)
from django.db.models import Sum

from apps.informes.filter import InformesFilter
from apps.core.analytics import Report

from apps.core.models import (
	Operacion,
	Cuenta
)

from ..base import (
	AdminListObjectsView,
	AdminRegistroView,
	AdminParametrosCUDView
)

from . import config


class IndexView(AdminListObjectsView):

	""" Vista de contabilidad """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	MODULE_FIELD_DISPLAY = ['id', 'numero', 'nombre', 'supertitulo']
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"	
	filterset_class = InformesFilter

	def get_operaciones(self):
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


	def get_all_titulo(self):
		queryset = self.get_operaciones()
		objects = super().get_all_titulo()
		for o in objects:
			o['debe'] = queryset.filter(cuenta__titulo_id=o['id'], valor__gte=0).aggregate(debe=Sum('valor'))['debe'] or \
						queryset.filter(cuenta__titulo__supertitulo_id=o['id'], valor__gte=0).aggregate(debe=Sum('valor'))['debe'] or 0
			o['haber'] = queryset.filter(cuenta__titulo_id=o['id'], valor__lte=0).aggregate(haber=Sum('valor'))['haber'] or \
						queryset.filter(cuenta__titulo__supertitulo_id=o['id'], valor__lte=0).aggregate(haber=Sum('valor'))['haber'] or 0
			o['haber'] = -o['haber']
			o['saldo'] = o['debe'] - o['haber']
		return objects

class CUDParametroView(
		AdminParametrosCUDView, 
		generic.CreateView,
		generic.UpdateView,
	):

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	template_name = f'{config.TEMPLATE_FOLDER}/cu-object.html'	

class RegistroView(AdminRegistroView):

	""" Vista de registro de comprobantes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	INITAL_FILTERS = {'receipt__receipt_type__description':'Asiento'}
	ORDER_BY = '-receipt__receipt_number'
	template_name = f'{config.TEMPLATE_FOLDER}/registros.html'		

	
class MayoresView(AdminRegistroView):

	""" Base registros de comprobantes """
	
	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	SUBMODULE = {'name': 'Mayores'}
	ORDER_BY = '-pk'
	model = Operacion
	filterset_class = InformesFilter
	template_name = f'{config.TEMPLATE_FOLDER}/mayores.html'	

	def get_queryset(self):
		any_filters = any(self.request.GET.values())
		if any_filters:		
			datos = Operacion.objects.filter(
				comunidad=self.comunidad,
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
		else:
			datos = Operacion.objects.none()
		self.filter = self.filterset_class(self.request.GET, queryset=datos)
		return self.filter.qs

	def get(self, *args, **kwargs):
		""" Para la exportación a excel """
		any_filters = any(self.request.GET.values())
		if any_filters:
			queryset = self.get_queryset()
			df = Report(
					comunidad=self.comunidad,
					data=queryset
				).get_df(raw_data=True)
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

		return super().get(*args, **kwargs)
