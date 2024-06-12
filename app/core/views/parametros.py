from django.http import Http404
from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django_afip.models import PointOfSales

from users.permissions import IsAccountOwner, IsComunidadMember, IsAdministrativoUser
from utils.generics import custom_viewsets
from core.serializers import (
	CuentaModelSerializer,
	TituloModelSerializer,
	PuntoModelSerializer,
	ProyectoModelSerializer
)

from core.models import (
	Cuenta,
	Titulo,
	Naturaleza,
	Proyecto
)

try:
	CUENTAS = list(Naturaleza.objects.all().values_list('nombre', flat=True))
except:
	CUENTAS = []


class ParametrosViewSet(custom_viewsets.CustomModelViewSet):
	'''
	Parametros View Set.
	Crea, actualiza, detalla y lista Cuentas de diferentes naturaleza.
	Crea, actualiza, detalla y lista Titulos.
	Crea, actualiza, detalla y lista Comprobantes.
	Deudas pendientes de cancelacion para Clientes y Proveedores.
	'''

	# filterset_class = OperacionFilter

	def get_queryset(self):
		'''Define el queryset segun parametro de url.'''
		try:
			if self.kwargs['naturaleza'] in CUENTAS:
				queryset = Cuenta.all_objects.filter(
					comunidad=self.comunidad, 
					naturaleza__nombre=self.kwargs['naturaleza']
				).select_related(
				"perfil", 
				'perfil__domicilio',
				"titulo",
				"taxon",
				"domicilio"
				)
			elif self.kwargs['naturaleza'] == 'titulo':
				queryset = Titulo.all_objects.filter(
					comunidad=self.comunidad
				).select_related(
					"supertitulo",
					"predeterminado"
				).prefetch_related(
					"cuenta_set"
				)
			elif self.kwargs['naturaleza'] == 'punto':
				queryset = PointOfSales.objects.filter(
					owner=self.comunidad.contribuyente
				)		
			elif self.kwargs['naturaleza'] == 'proyecto':
				queryset = Proyecto.all_objects.filter(
					comunidad=self.comunidad
				)
			if self.request.GET.get('archived', False):
				return queryset.dead()
			return queryset.alive()
		except:
			raise Http404

	def get_serializer_class(self):
		'''Define el serializer segun parametro de url.'''
		try:
			return {
				'cliente': CuentaModelSerializer,
				'proveedor': CuentaModelSerializer,
				'caja': CuentaModelSerializer,
				'ingreso': CuentaModelSerializer,
				'gasto': CuentaModelSerializer,
				'titulo': TituloModelSerializer,
				'punto': PuntoModelSerializer,
				'proyecto': ProyectoModelSerializer
			}[self.kwargs['naturaleza']]
		except:
			raise Http404

	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsAdministrativoUser]
		if self.action in ['update', 'retrieve']:
			permissions.append(IsComunidadMember)
		if self.kwargs['naturaleza'] == 'punto' and self.action != "list":
			permissions.append(IsAccountOwner)
			
		return [p() for p in permissions]

	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		serializer_context['naturaleza'] = self.kwargs['naturaleza']
		return serializer_context

	def create(self, request, naturaleza=None):
		is_many = isinstance(request.data, list)

		serializer = self.get_serializer(data=request.data, many=is_many)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	@action(detail=False, methods=['get'])
	def total(self, request, *args, **kwargs):
		""" Devulve todas las cuentas """
		return Response(status=status.HTTP_201_CREATED)