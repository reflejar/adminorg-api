from ..base import AdminFrontView
from ..configuracion.views import ListView

from .buttons import MODULE_BUTTONS

class IndexView(ListView):

	""" Vista de clientes """

	# model = Liquidacion
	# filterset_class = LiquidacionFilter
	MODULE_NAME = "Cuentas a cobrar"
	MODULE_NATURALEZA = "cliente"
	MODULE_BUTTONS = MODULE_BUTTONS
	template_name = 'contents/list-objects.html'	

	def get_objects(self):
		objects = super().get_objects()
		for o in objects:
			o.pop("titulo_contable")
			o.pop("razon_social")
			o.pop("tipo_documento")
		return objects

	def get_context_data(self, **kwargs):
		kwargs['naturaleza'] = self.MODULE_NATURALEZA
		context = super().get_context_data(**kwargs)
		return context

	