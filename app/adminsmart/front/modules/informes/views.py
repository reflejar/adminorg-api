from django.views import generic

from adminsmart.front.modules.clientes.views import IndexView as ClientesModule
from adminsmart.front.modules.proveedores.views import IndexView as ProveedoresModule
from adminsmart.front.modules.tesoreria.views import IndexView as TesoreriaModule
from adminsmart.front.modules.forms import InformeForm


from ..base import (
	BaseAdminView,
	BaseCUDView
)

from . import config

class IndexView(BaseAdminView):

	""" Vista index de informes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = ""
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"
	MODULES_CHARTS = {
		'cuentas-a-cobrar': ClientesModule.MODULE_CHART,
		'cuentas-a-pagar': ProveedoresModule.MODULE_CHART,
		'tesoreria': TesoreriaModule.MODULE_CHART,
	}
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['charts'] = [c for m,c in self.MODULES_CHARTS.items() if m in self.allowed_modules]
		for c in context['charts']:
			c.comunidad = self.comunidad
		return context	

class CUDView(
		BaseCUDView,
		generic.CreateView,
	):

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	template_name = f'{config.TEMPLATE_FOLDER}/cu-object.html'

	FORMS = {
		'informes': InformeForm,
	}

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['context'].update({'comunidad':self.comunidad})
		return kwargs