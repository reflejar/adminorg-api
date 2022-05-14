from ..base import (
	AdminModuleView,
	AdminEstadoView
)

from .buttons import MODULE_BUTTONS

MODULE = {
	'name': "Cuentas a cobrar",
	'path': 'front:clientes:index'
}

class IndexView(AdminModuleView):

	""" Vista de clientes """

	MODULE = MODULE
	MODULE_BUTTONS = MODULE_BUTTONS
	MODULE_HANDLER = "cliente"
	MODULE_FIELD_DISPLAY = ['id', 'apellido_cliente', 'nombre_cliente', 'razon_social']
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de clientes """

	MODULE = MODULE
	SUBMODULE = {'name': 'Detalle de deudas'}
	MODULE_HANDLER = "estado_deuda"
	MODULE_BUTTONS = MODULE_BUTTONS

class EstadoCuentaView(AdminEstadoView):

	""" Vista de clientes """

	MODULE = MODULE
	SUBMODULE = {'name': 'Cuenta histórica'}
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = MODULE_BUTTONS