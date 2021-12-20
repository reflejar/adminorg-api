from datetime import datetime, date
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from decimal import Decimal

from adminsmart.users.permissions import IsAccountOwner, IsComunidadMember, IsAdministrativoUser
from adminsmart.utils.generics import custom_viewsets

from adminsmart.operative.filters.operacion import OperacionFilter

from adminsmart.operative.models import (
	Naturaleza,
	Cuenta,
	Operacion,
	Titulo
)

from adminsmart.operative.serializers.estados import (
	EstadoCuentaSerializer,
	EstadoDeudasSerializer,
	EstadoSaldosSerializer
)

class EstadosViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Estado de cuenta para Clientes, Proveedores y Cajas.
		Deudas pendientes de cancelacion para Clientes y Proveedores.
	"""
	
	http_method_names = ['get']

	filterset_class = OperacionFilter

	SERIALIZERS = {
		'cuenta': EstadoCuentaSerializer,
		'deudas': EstadoDeudasSerializer,
		'saldos': EstadoDeudasSerializer # Si existe la necesidad de tener separados los saldos de las deudas aunque utilicen el mismo serializer
	}

	def get_queryset(self, **kwargs):
		fecha = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date() if 'end_date' in self.request.GET.keys() else date.today()
		obj = self.get_object()
		if self.kwargs['tipo'] == "deudas":
			datos = obj.estado_deuda(fecha=fecha)
		elif self.kwargs['tipo'] == "cuenta":
			datos = obj.estado_cuenta(fecha=fecha)
		elif self.kwargs['tipo'] == "saldos":
			datos = obj.estado_saldos(fecha=fecha)

		self.filter = self.filterset_class(self.request.GET, queryset=datos)
		return self.filter.qs

	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsComunidadMember]
		if self.request.user.groups.all()[0].name == "socio":
			permissions.append(IsAccountOwner)
		else:
			permissions.append(IsAdministrativoUser)
		return [p() for p in permissions]

	def get_object(self):
		if 'titulo' in self.request.GET.keys():
			obj = get_object_or_404(
					Titulo.objects.filter(comunidad=self.comunidad), 
					pk=self.kwargs["pk"]
				)
		else:
			obj = get_object_or_404(
					Cuenta.objects.filter(comunidad=self.comunidad), 
					pk=self.kwargs["pk"]
				)
		self.check_object_permissions(self.request, obj)
		return obj
		
	def get_serializer_class(self):
		'''Define el serializer segun parametro de url.'''
		try:
			return self.SERIALIZERS[self.kwargs['tipo']]
		except:
			raise Http404

	def retrieve(self, request, pk=None, **kwargs):
		queryset = self.get_queryset()
		filtro = self.filter.data
		end_date = filtro['end_date'] if 'end_date' in filtro.keys() else date.today()
		end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		context = {
			'end_date': end_date,
			'condonacion': True if 'condonacion' in filtro.keys() else False,
			'cuenta': self.get_object()
		}
		serializer = self.get_serializer_class()(queryset, context)
		return Response(reversed(serializer.data))