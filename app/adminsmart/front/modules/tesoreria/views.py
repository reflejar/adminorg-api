from ..base import (
	AdminModuleView,
	AdminEstadoView
)

from .buttons import MODULE_BUTTONS

class IndexView(AdminModuleView):

	""" Vista de clientes """

	MODULE_NAME = "Tesoreria"
	MODULE_HANDLER = "caja"
	MODULE_BUTTONS = MODULE_BUTTONS
	MODULE_FIELD_DISPLAY = ['id', 'nombre', 'tipo']
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de clientes """

	MODULE_NAME = "Tesoreria"
	MODULE_HANDLER = "estado_deuda"
	MODULE_BUTTONS = MODULE_BUTTONS

class EstadoCuentaView(AdminEstadoView):

	""" Vista de clientes """

	MODULE_NAME = "Tesoreria"
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = MODULE_BUTTONS