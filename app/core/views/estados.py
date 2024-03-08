import json
from datetime import datetime, date
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from decimal import Decimal

from users.permissions import IsAccountOwner, IsComunidadMember, IsAdministrativoUser
from utils.generics import custom_viewsets

from core.filters.operacion import OperacionFilter

from core.models import (
	Naturaleza,
	Cuenta,
	Operacion,
	Titulo
)


class EstadosViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Estado de cuenta para Clientes, Proveedores y Cajas.
		Deudas pendientes de cancelacion para Clientes y Proveedores.
	"""
	
	http_method_names = ['get']

	filterset_class = OperacionFilter


	def get_queryset(self, **kwargs):
		fecha = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date() if 'end_date' in self.request.GET.keys() else date.today()
		obj = self.get_object()
		if self.kwargs['tipo'] == "saldos":
			datos = Cuenta.saldos(cuentas=obj, fecha=fecha)
		elif self.kwargs['tipo'] == "movimientos":
			datos = Cuenta.mayores(cuentas=obj,fecha=fecha)
		return datos

	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsComunidadMember]
		if self.request.user.groups.all()[0].name == "socio":
			permissions.append(IsAccountOwner)
		else:
			permissions.append(IsAdministrativoUser)
		return [p() for p in permissions]

	def get_object(self):
		if self.kwargs["pk"].isdigit():
			if 'titulo' in self.request.GET.keys():
				titulo = Titulo.objects.get(id=self.kwargs["pk"])
				obj = Cuenta.objects.filter(comunidad=self.comunidad, titulo=titulo)
			else:
				obj = Cuenta.objects.filter(comunidad=self.comunidad, pk=self.kwargs["pk"])
		else:
			obj = Cuenta.objects.filter(comunidad=self.comunidad)
		# self.check_object_permissions(self.request, obj)
		return obj
		

	def retrieve(self, request, pk=None, **kwargs):
		queryset = self.get_queryset()
		# filtro = self.filter.data
		return Response({'data': json.loads(queryset.to_json(orient="records"))})

		end_date = filtro['end_date'] if 'end_date' in filtro.keys() else date.today()
		end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
		context = {
			'end_date': end_date,
			'cuenta': self.get_object()
		}
		# paginator_response = {}
		# if 'page' in filtro.keys():
		# 	try:

		# 		paginator = Paginator(queryset, 15)
		# 		queryset = paginator.page(filtro['page'])
		# 		paginator_response.update({
		# 			'has_previous': queryset.has_previous(),
		# 			'has_next': queryset.has_next(),
		# 			'num_pages': paginator.num_pages
		# 		})
		# 	except:
		# 		pass
			
		
		serializer = self.get_serializer_class()(queryset, context)
		return Response({'data': serializer.data})
		# return Response({'data': serializer.data, 'paginator': paginator_response})