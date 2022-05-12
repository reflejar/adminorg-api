from ..base import AdminFrontView

from .buttons import MODULE_BUTTONS

class IndexView(AdminFrontView):

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
	