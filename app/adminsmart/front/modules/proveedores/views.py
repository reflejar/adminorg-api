from django.views import generic

from adminsmart.front.modules import charts

from ..base import (
	AdminListObjectsView,
	AdminEstadoView,
	AdminRegistroView,
	AdminParametrosCUDView
)

from . import config

class IndexView(AdminListObjectsView):

	""" Vista de proveedores """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	MODULE_FIELD_DISPLAY = ['id', 'apellido_proveedor', 'nombre_proveedor', 'razon_social']
	MODULE_CHART = charts.Pie('a_pagar')
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"


class CUDParametroView(
		AdminParametrosCUDView, 
		generic.CreateView,
		generic.UpdateView,
	):

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	template_name = f'{config.TEMPLATE_FOLDER}/cu-object.html'	
	
class EstadoDeudasView(AdminEstadoView):

	""" Vista de estado de deudas """

	MODULE = config.MODULE
	SUBMODULE = {'name': 'Detalle de deudas'}
	MODULE_HANDLER = "estado_deuda"
	MODULE_BUTTONS = config.MODULE_BUTTONS
	EDIT_URL = 'front:proveedores:cbte-edit'		
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'			

class EstadoCuentaView(AdminEstadoView):

	""" Vista de estado de cuenta """

	MODULE = config.MODULE
	SUBMODULE = {'name': 'Cuenta histórica'}
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = config.MODULE_BUTTONS
	EDIT_URL = 'front:proveedores:cbte-edit'		
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'			


class RegistroView(AdminRegistroView):

	""" Vista de registro de comprobantes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	template_name = f'{config.TEMPLATE_FOLDER}/registros.html'
	INITAL_FILTERS = {'destinatario__naturaleza__nombre':'proveedor'}