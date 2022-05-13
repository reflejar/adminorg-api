from ..base import (
	AdminModuleView,
	AdminEstadoView
)

from .buttons import MODULE_BUTTONS

class IndexView(AdminModuleView):

	""" Vista de clientes """

	MODULE_NAME = "Cuentas a cobrar"
	MODULE_HANDLER = "cliente"
	MODULE_BUTTONS = MODULE_BUTTONS
	MODULE_FIELD_DISPLAY = ['id', 'apellido_cliente', 'nombre_cliente', 'razon_social']
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de clientes """

	MODULE_NAME = "Cuentas a cobrar"
	MODULE_HANDLER = "estado_deuda"
	MODULE_BUTTONS = MODULE_BUTTONS

class EstadoCuentaView(AdminEstadoView):

	""" Vista de clientes """

	MODULE_NAME = "Cuentas a cobrar"
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = MODULE_BUTTONS