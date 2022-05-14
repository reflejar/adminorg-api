from ..base import (
	AdminModuleView,
	AdminEstadoView
)

from .buttons import MODULE_BUTTONS

MODULE = {
	'name': "Tesoreria",
	'path': 'front:tesoreria:index'
}

class IndexView(AdminModuleView):

	""" Vista de clientes """

	MODULE = MODULE
	MODULE_BUTTONS = MODULE_BUTTONS
	MODULE_HANDLER = "caja"
	MODULE_FIELD_DISPLAY = ['id', 'nombre', 'tipo']
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de clientes """

	MODULE = MODULE
	SUBMODULE = {'name': 'Detalle de deudas'}
	MODULE_BUTTONS = MODULE_BUTTONS
	MODULE_HANDLER = "estado_deuda"

class EstadoCuentaView(AdminEstadoView):

	""" Vista de clientes """

	MODULE = MODULE
	SUBMODULE = {'name': 'Cuenta histórica'}
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = MODULE_BUTTONS