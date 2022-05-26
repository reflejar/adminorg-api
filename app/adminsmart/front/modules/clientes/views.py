from django.views import generic

from ..base import (
	AdminListObjectsView,
	AdminEstadoView,
	AdminRegistroView,
	AdminCUDView
)

from . import config

class IndexView(AdminListObjectsView):

	""" Vista de clientes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	MODULE_HANDLER = config.MODULE_HANDLER
	MODULE_FIELD_DISPLAY = ['id', 'apellido_cliente', 'nombre_cliente', 'razon_social']
	template_name = f"{config.TEMPLATE_FOLDER}/index.html"
	


class CUDObjectView(
		AdminCUDView, 
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
	EDIT_URL = 'front:clientes:cbte-edit'			
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'

class EstadoCuentaView(AdminEstadoView):

	""" Vista de estado de cuenta """

	MODULE = config.MODULE
	SUBMODULE = {'name': 'Cuenta histórica'}
	MODULE_HANDLER = "estado_cuenta"
	MODULE_BUTTONS = config.MODULE_BUTTONS
	EDIT_URL = 'front:clientes:cbte-edit'		
	template_name = f'{config.TEMPLATE_FOLDER}/estados.html'	


class RegistroView(AdminRegistroView):

	""" Vista de registro de comprobantes """

	MODULE = config.MODULE
	MODULE_BUTTONS = config.MODULE_BUTTONS
	template_name = f'{config.TEMPLATE_FOLDER}/registros.html'
	INITAL_FILTERS = {'destinatario__naturaleza__nombre':'cliente'}