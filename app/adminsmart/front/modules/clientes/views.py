from ..base import AdminFrontView

from .buttons import MODULE_BUTTONS

class IndexView(AdminFrontView):

	""" Vista de clientes """

	# model = Liquidacion
	# filterset_class = LiquidacionFilter
	MODULE_NAME = "Cuentas a cobrar"
	MODULE_NATURALEZA = "cliente"
	MODULE_BUTTONS = MODULE_BUTTONS

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
