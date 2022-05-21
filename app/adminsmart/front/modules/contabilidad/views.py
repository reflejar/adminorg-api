import tempfile
import pandas as pd
from django.http import (
	Http404,
	FileResponse
)
from django.db.models import Sum

from adminsmart.apps.informes.filter import InformesFilter
from adminsmart.apps.core.models import Operacion

from ..base import (
	AdminListObjectsView,
	AdminRegistroView,
)

from . import config


class IndexView(AdminListObjectsView):

	""" Vista de contabilidad """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = "titulo"
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

	def get(self, *args, **kwargs):
		""" Para la exportación a excel """
		return super().get(*args, **kwargs)
