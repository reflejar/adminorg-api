from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django_afip.models import (
	ReceiptType,
	PointOfSales
)
from admincu.users.permissions import IsAccountOwner, IsComunidadMember, IsAdministrativoUser
from admincu.utils.generics import custom_viewsets
from admincu.operative.serializers import (
	CuentaModelSerializer,
	TituloModelSerializer,
	MetodoModelSerializer,
	DocumentoModelSerializer,
	PuntoModelSerializer
)
from admincu.operative.serializers.estados import (
	EstadoDeudasModelSerializer,
	EstadoCuentaModelSerializer

)
from admincu.operative.models import (
	Cuenta,
	Operacion,
	Metodo,
	Titulo,
	Documento,
	Naturaleza,
)
from admincu.operative.filters import (
	ClienteFilter,
	OperacionFilter
)


class ParametrosViewSet(custom_viewsets.CustomModelViewSet):
	'''
	Parametros View Set.
	Crea, actualiza, detalla y lista Cuentas de diferentes naturaleza.
	Crea, actualiza, detalla y lista Titulos.
	Crea, actualiza, detalla y lista Metodos.
	Crea, actualiza, detalla y lista Documentos.
	Estado de cuenta para Clientes, Proveedores y Cajas.
	Deudas pendientes de cancelacion para Clientes y Proveedores.
	'''
	cuentas = list(Naturaleza.objects.all().values_list('nombre', flat=True))
	titulos = ['titulo']
	metodos = ['interes', 'retencion', 'descuento']
	puntos = ['punto']

	# filterset_class = OperacionFilter

	def get_queryset(self):
		'''Define el queryset segun parametro de url.'''
		try:
			if self.kwargs['naturaleza'] in self.cuentas:
				queryset = Cuenta.objects.filter(comunidad=self.comunidad, naturaleza__nombre=self.kwargs['naturaleza'])
			elif self.kwargs['naturaleza'] in self.titulos:
				queryset = Titulo.objects.filter(comunidad=self.comunidad)
			elif self.kwargs['naturaleza'] in self.metodos:
				queryset = Metodo.objects.filter(comunidad=self.comunidad, naturaleza=self.kwargs['naturaleza'])
			elif self.kwargs['naturaleza'] in self.puntos:
				queryset = PointOfSales.objects.filter(owner=self.comunidad.contribuyente)				
			return queryset
		except:
			raise Http404


	def get_serializer_class(self):
		'''Define el serializer segun parametro de url.'''
		try:
			if self.kwargs['naturaleza'] in self.cuentas:
				serializer_class = CuentaModelSerializer
			elif self.kwargs['naturaleza'] in self.titulos:
				serializer_class = TituloModelSerializer
			elif self.kwargs['naturaleza'] in self.metodos:
				serializer_class = MetodoModelSerializer
			elif self.kwargs['naturaleza'] in self.puntos:
				serializer_class = PuntoModelSerializer								
			return serializer_class
		except:
			raise Http404


	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsAdministrativoUser]
		if self.action in ['update', 'retrieve']:
			permissions.append(IsComunidadMember)
		if self.kwargs['naturaleza'] in self.puntos and self.action != "list":
			permissions.append(IsAccountOwner)
			
		return [p() for p in permissions]


	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		serializer_context['naturaleza'] = self.kwargs['naturaleza']
		return serializer_context



	@action(detail=False, methods=['get'])
	def total(self, request, *args, **kwargs):
		""" Devulve todas las cuentas """
		
		return Response(status=status.HTTP_201_CREATED)
