from ..base import (
	AdminListObjectsView,
	AdminEstadoView,
	AdminRegistroView
)

from . import config

class IndexView(AdminListObjectsView):

	""" Vista de tesoreria """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = "caja"
	MODULE_FIELD_DISPLAY = ['id', 'nombre', 'tipo']
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de estado de deudas """

	MODULE = config.MODULE
	SUBMODULE = {'name': 'Stock de disponibilidades'}
	MODULE_HANDLER = "estado_deuda"
	MODULE_BUTTONS = config.MODULE_BUTTONS
	EDIT_URL = 'front:tesoreria:cbte-edit'		
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'			

class EstadoCuentaView(AdminEstadoView):

	""" Vista de estado de cuenta """

	MODULE = config.MODULE
	SUBMODULE = {'name': 'Movimientos'}
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = config.MODULE_BUTTONS
	EDIT_URL = 'front:tesoreria:cbte-edit'		
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'			


class RegistroView(AdminRegistroView):

	""" Vista de registro de comprobantes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	template_name = f'{config.TEMPLATE_FOLDER}/registros.html'