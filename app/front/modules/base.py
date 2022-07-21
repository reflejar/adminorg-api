from itertools import groupby

from django.db.models import F
from django.http import Http404
from django.views import generic
from django.core.cache import cache
from django.shortcuts import get_object_or_404 
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings

from django_afip.models import ReceiptType

from apps.core.models import (
	Cuenta,
	Metodo,
	Titulo,
	Documento,
	Operacion
)

from apps.core.filters import (
	DocumentoFilter
)

from ..permissions import (
	CommunityPermissions,
	UserObjectCommunityPermissions,
	ModulePermissions
)

from .forms import (
	CuentaForm,
	TituloForm,
	MetodoForm,
	DocumentoClienteForm,
	DocumentoProveedorForm,
	DocumentoTesoreriaForm
)

class BaseFrontView(CommunityPermissions, ModulePermissions, generic.TemplateView):

	""" Base Front """
	
	template_name = 'layout.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			'comunidad': self.comunidad,
			'allowed_modules': "/".join(self.allowed_modules)
		})
		if getattr(self, "MODULE", False):
			context.update({'module': self.MODULE})
		if getattr(self, "SUBMODULE", False):
			context.update({'submodule': self.SUBMODULE})
		if getattr(self, "MODULE_BUTTONS", False):
			context.update({'side_buttons': self.MODULE_BUTTONS})	
		if getattr(self, "MODULE_HANDLER", False):
			context.update({'module_handler': self.MODULE_HANDLER})					
		if getattr(self, "MODULE_CHART", False):
			self.MODULE_CHART.comunidad = self.comunidad
			context.update({'side_chart': self.MODULE_CHART})
		return context

class BaseAdminView(BaseFrontView):

	""" Base Admin Front """

	def make_cache_key(self): return f'views_{self.MODULE_HANDLER}_{self.comunidad.id}'

	def get_objects(self): # Funcion pensada para cachear
		method = getattr(self, f"get_all_{self.MODULE_HANDLER}")
		return method()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if getattr(self, "MODULE_HANDLER", False):
			objects = self.get_objects()
			context.update({
				"objects": objects,
				"titles": objects[0].keys() if objects else []
			})
		return context

class AdminListObjectsView(BaseAdminView):

	""" Base obtencion de objetos de los modulos """

	template_name = 'contents/list-objects.html'

	def get_all_titulo(self):
		default_fields = [
			'id', 'numero','nombre',
			'predeterminado_para'
		]
		field_display = self.MODULE_FIELD_DISPLAY \
						if getattr(self, 'MODULE_FIELD_DISPLAY', None) \
						else default_fields				
		return list(Titulo.objects.filter(comunidad=self.comunidad)\
			.order_by("numero")\
			.annotate(predeterminado_para=F('predeterminado__nombre'))\
			.values(
				*field_display
			))
		
	def get_all_caja(self): 
		default_fields = ['id', 'nombre', 'tipo', 'titulo_contable']
		field_display = self.MODULE_FIELD_DISPLAY \
						if getattr(self, 'MODULE_FIELD_DISPLAY', None) \
						else default_fields		
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_HANDLER)\
					.order_by("nombre")\
					.annotate(
						tipo=F('taxon__nombre'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						*field_display
					))		
	get_all_gasto = get_all_caja	
	get_all_bien_de_cambio = get_all_caja

	def get_all_ingreso(self):
		cuentas = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_HANDLER)\
			.order_by("nombre")\
			.annotate(
				metodos_descuento_interes=F('metodos__nombre'),
				titulo_contable=F('titulo__nombre'),
			)\
			.values(
				'id', 'nombre', 'metodos_descuento_interes', 'titulo_contable'
			)				
		
		objects = []
		for _, value in groupby(cuentas, lambda x: x['nombre']):
			parsed_object = list(value)
			primary_object = parsed_object[0].copy()
			if len(parsed_object) > 1:
				primary_object['metodos_descuento_interes'] = ", ".join(o["metodos_descuento_interes"] for o in parsed_object)
			objects.append(primary_object)
		return objects		

	def get_all_interes(self):
		return list(Metodo.objects.filter(comunidad=self.comunidad, naturaleza=self.MODULE_HANDLER)\
				.order_by('-id')\
				.values(
				'id',"nombre","tipo",
				"plazo","monto",
				))
	get_all_descuento = get_all_interes
	

	def get_all_cliente(self): 
		default_fields = [
			'id', 'apellido_cliente','nombre_cliente',
			'razon_social', 'tipo_documento','documento','titulo_contable'
		]
		field_display = self.MODULE_FIELD_DISPLAY \
						if getattr(self, 'MODULE_FIELD_DISPLAY', None) \
						else default_fields
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_HANDLER)\
					.order_by("perfil__apellido")\
					.annotate(
						apellido_cliente=F('perfil__apellido'),
						nombre_cliente=F('perfil__nombre'),
						razon_social=F('perfil__razon_social'),
						tipo_documento=F('perfil__tipo_documento__description'),
						documento=F('perfil__numero_documento'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						*field_display
					))		

	def get_all_proveedor(self): 
		default_fields = [
			'id', 'razon_social','apellido_proveedor','nombre_proveedor',
			'tipo_documento','documento','titulo_contable',
		]
		field_display = self.MODULE_FIELD_DISPLAY \
						if getattr(self, 'MODULE_FIELD_DISPLAY', None) \
						else default_fields		
		return list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_HANDLER)\
					.order_by("perfil__razon_social", "perfil__apellido")\
					.annotate(
						razon_social=F('perfil__razon_social'),
						apellido_proveedor=F('perfil__apellido'),
						nombre_proveedor=F('perfil__nombre'),
						tipo_documento=F('perfil__tipo_documento__description'),
						documento=F('perfil__numero_documento'),
						titulo_contable=F('titulo__nombre'),						
					)\
					.values(
						*field_display
					))		

	def get_all_dominio(self): 
		cuentas = list(Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.MODULE_HANDLER)\
					.order_by('numero')\
					.values(
						'id', 'numero', 
						'vinculo2__cuenta__perfil__apellido','vinculo2__cuenta__perfil__nombre', 
						'vinculo2__definicion__nombre'
					))	
		objects = []
		for _, value in groupby(cuentas, lambda x: x['numero']):
			parsed_object = list(value)
			primary_object = parsed_object[0].copy()
			primary_object['relaciones'] = ", ".join(
				f'{o["vinculo2__definicion__nombre"]}: {o["vinculo2__cuenta__perfil__apellido"]}, {o["vinculo2__cuenta__perfil__nombre"]}' for o in parsed_object
			)
			objects.append(primary_object)
			primary_object.pop("vinculo2__definicion__nombre")
			primary_object.pop("vinculo2__cuenta__perfil__apellido")
			primary_object.pop("vinculo2__cuenta__perfil__nombre")
		return objects						

	def get_all_grupo(self): return []

class AdminEstadoView(
		BaseAdminView, 
		UserObjectCommunityPermissions, 
		generic.detail.SingleObjectMixin
	):

	""" Base obtencion de estados de los modulos """
	
	template_name = 'contents/estados.html'	

	def get_all_estado_deuda(self):	
		""" PROBLEMA A SOLUCIONAR: LA ITERACION"""
		deudas = []
		for o in self.object.estado_deuda():
			pago_capital = o.pago_capital()
			interes = o.interes()
			descuento = o.descuento()
			receipt_type = str(o.documento.receipt.receipt_type)
			formatted_number = str(o.documento.receipt.formatted_number)
			saldo = o.monto - pago_capital + interes - descuento
			deudas.append({
				'cuenta_id': o.cuenta.id,
				'documento_id': o.documento.id,
				'fecha': o.fecha,
				'fecha_anulacion': o.documento.fecha_anulacion,
				'tipo_comprobante': receipt_type,
				'numero': formatted_number,
				'cuenta': str(o.cuenta),
				'concepto': str(o.concepto()), 
				'periodo': o.periodo(),
				'monto': o.monto,
				'pago_capital': pago_capital,
				'interes': interes,
				'saldo': saldo,
				'pdf': o.id if o.documento.pdf else None
			})
			
		return deudas
	
	def get_all_estado_cuenta(self):	
		cuenta = []
		saldo = 0
		for d in self.object.estado_cuenta():
			receipt_type = str(d.receipt.receipt_type)
			formatted_number = str(d.receipt.formatted_number)
			total = sum([o.valor for o in d.operaciones.all() if o.cuenta in self.object.grupo])
			# if isinstance(obj, Cuenta):
			# 	total = sum([o.valor for o in d.operaciones.all() if o.cuenta in obj.grupo])
			# else:
			# 	total = sum([o.valor for o in d.operaciones.all() if o.cuenta.titulo in obj.grupo])
			saldo += total
			cuenta.append({
				'cuenta_id': d.destinatario.id if d.destinatario else None,
				'documento_id': d.id,
				'fecha': d.fecha_operacion,
				'fecha_anulacion': d.fecha_anulacion,
				'tipo_comprobante': receipt_type,
				'numero': formatted_number,
				'total': total,
				'saldo': saldo,
				'pdf': d.id if d.pdf else None
			}) 

		return list(reversed(cuenta))

	def get_object(self):
		return get_object_or_404(
			Cuenta.objects.filter(comunidad=self.comunidad),
			pk=self.kwargs['pk']
		)

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = super().get_context_data(**kwargs)
		if getattr(self, 'EDIT_URL', None):
			context.update({'edit_url': self.EDIT_URL})
		return context		

class AdminRegistroView(BaseAdminView, generic.ListView):

	""" Base registros de comprobantes """
	
	model = Documento
	filterset_class = DocumentoFilter
	paginate_by = 100
	template_name = 'contents/registros.html'	
	INITAL_FILTERS = {}
	SUBMODULE = {'name': 'Registro de comprobantes'}
	ORDER_BY = '-receipt__issued_date'


	def get_queryset(self, **kwargs):
		datos = self.model.objects.filter(comunidad=self.comunidad, **self.INITAL_FILTERS).order_by(self.ORDER_BY)
		self.filter = self.filterset_class(self.request.GET, queryset=datos)
		return self.filter.qs

	def get_context_data(self, **kwargs):
		self.object_list = self.get_queryset()
		context = super().get_context_data(**kwargs)
		context['filter'] = self.filter
		datos = self.filter.qs
		if datos or self.request.GET.get('page'):
			paginador = Paginator(datos, self.paginate_by)
			pagina = self.request.GET.get('page')
			context['lista'] = paginador.get_page(pagina)
		else:
			context['is_paginated'] = False
			context['lista'] = datos
		return context

class BaseCUDView(BaseFrontView):

	MODELS = {
		'cliente': Cuenta,
		'proveedor': Cuenta,
		'dominio': Cuenta,
		'grupo': Cuenta,
		'caja': Cuenta,
		'ingreso': Cuenta,
		'gasto': Cuenta,
		'bien_de_cambio': Cuenta,
		'titulo': Titulo,
		'interes': Metodo,
		'descuento': Metodo,
		'documento_cliente': Documento,
		'informes': Operacion,
	}	

	@property
	def SUBMODULE(self):
		if 'pk' in self.kwargs.keys():
			return {'name': f'Editar {self.MODULE_HANDLER}'}
		return {'name': f'Nuevo {self.MODULE_HANDLER}'}		

	def get_form_class(self):
		return self.FORMS[self.MODULE_HANDLER]

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['context'] = {
			'comunidad': self.comunidad,
			'request': self.request,
		}
		return kwargs

	def get_object(self):
		if not 'pk' in self.kwargs.keys():
			return None
		return get_object_or_404(
			self.MODELS[self.MODULE_HANDLER].objects.filter(comunidad=self.comunidad),
			pk=self.kwargs['pk']
		)		

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = super().get_context_data(**kwargs)
		return context

	@transaction.atomic
	def form_valid(self, form):
		mensaje = "{} guardado con exito".format(self.MODULE_HANDLER)
		messages.success(self.request, mensaje)
		return super().form_valid(form)		

	def get_success_url(self, **kwargs):
		if self.MODULE['path'] == "front:configuracion:index":
			return reverse_lazy('front:configuracion:list', args=(self.MODULE_HANDLER,))		
		return reverse_lazy(self.MODULE['path'])	

class AdminParametrosCUDView(BaseCUDView):

	FORMS = {
		'cliente': CuentaForm,
		'proveedor': CuentaForm,
		'dominio': CuentaForm,
		'grupo': CuentaForm,
		'caja': CuentaForm,
		'bien_de_cambio': CuentaForm,
		'ingreso': CuentaForm,
		'gasto': CuentaForm,
		'titulo': TituloForm,
		'interes': MetodoForm,
		'descuento': MetodoForm,
	}

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['context'].update({'naturaleza': self.MODULE_HANDLER})
		return kwargs
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.object and self.MODULE_HANDLER in ['interes', 'descuento']:
			context['disabled'] = "No se puede realizar esta acción"
		return context


class AdminDocumentosCUDView(BaseCUDView):

	FORMS = {
		'documento_cliente': DocumentoClienteForm,
		'documento_proveedor': DocumentoProveedorForm,
		'documento_caja': DocumentoTesoreriaForm,
	}	
	VERTICAL_STYLE = {'template_pack': 'rest_framework/vertical'}

	@property
	def RECEIPT_TYPE(self):
		receipt_type = self.request.GET.get('receipt_type')
		if self.object:
			return self.object.receipt.receipt_type
		elif receipt_type:
			return ReceiptType.objects.get(description=receipt_type)
		return ReceiptType()

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['context'].update({
			'sin_destinatario': False,
			'causante': self.MODULE_HANDLER.split("_")[1],
			'receipt_type': self.RECEIPT_TYPE,
		})
		if 'cuenta_pk' in self.request.GET:
			kwargs['context']['cuenta']	= Cuenta.objects.get(id=self.request.GET['cuenta_pk'])
		elif self.object.destinatario:
			kwargs['context']['cuenta'] = self.object.destinatario
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['vertical_style'] = self.VERTICAL_STYLE
		jsonify_choices = {}
		for k0,v0 in context['form'].fields.items():
			if getattr(v0, 'child', None) or getattr(v0, 'fields', None):
				jsonify_choices[k0] = {}
				if getattr(v0, 'fields', None):
					for k1,v1 in v0.fields.items():
						if getattr(v1, 'choices', None):
							jsonify_choices[k0][k1] = v1.choices
				if getattr(v0, 'child', None):
					for k1,v1 in v0.child.fields.items():
						if getattr(v1, 'choices', None):
							jsonify_choices[k0][k1] = v1.choices
		context['jsonify_choices'] = jsonify_choices
		context['react'] = settings.REACT
		return context

	def dispatch(self, request, *args, **kwargs):	
		if not 'cuenta_pk' in self.request.GET and not 'pk' in kwargs:
			raise Http404('There is no parameter cuenta_pk')
		return super().dispatch(request, *args, **kwargs)


	def form_invalid(self, form):
		print(form.errors)
		return super().form_invalid(form)

class SocioFrontView(BaseFrontView):

	""" Base Socio Front """


class BlankView(AdminListObjectsView):

	""" Vista blank """

	MODULE = {
		'name': "Plantilla",
		'path': 'front:index'
	}
	template_name = "layout.html"

