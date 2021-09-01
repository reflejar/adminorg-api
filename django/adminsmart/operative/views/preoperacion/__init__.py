from django.http import Http404
from django.shortcuts import get_object_or_404 
from django.db import transaction

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django_afip.models import (
	DocumentType,
	ReceiptType,
)
from adminsmart.users.permissions import IsComunidadMember, IsAdministrativoUser
from adminsmart.utils.generics import custom_viewsets
from adminsmart.operative.models import (
	PreOperacion
)
from adminsmart.operative.serializers.preoperaciones import PreOperacionesModelSerializer

class PreOperacionViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Para la carga de preconceptos
		Utiliza el serializer con 
			many=True si es POST
			many=False si es UPDATE
	"""

	serializer_class = PreOperacionesModelSerializer

	def get_queryset(self):
		return PreOperacion.objects.filter(
			comunidad=self.comunidad,
			fecha__isnull=True,
			cuenta__naturaleza__nombre__in=["cliente", "dominio"]
		)
		try:
			pass
		except:
			raise Http404

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj


	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsAdministrativoUser]
		if self.action in ['update', 'retrieve', 'delete']:
			permissions.append(IsComunidadMember)
		return [p() for p in permissions]

	
	def create(self, request, *args, **kwargs):
		for r in request.data:
			serializer = self.get_serializer(data=r)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
		return Response(status=status.HTTP_201_CREATED)

	# def create(self, request, *args, **kwargs):
	# 	is_many = isinstance(request.data, list)

	# 	serializer = self.get_serializer(data=request.data, many=True)
	# 	serializer.is_valid(raise_exception=True)
	# 	self.perform_create(serializer)
	# 	headers = self.get_success_headers(serializer.data)
	# 	return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	def list(self, request):
		queryset = self.get_queryset()
		context = {
			'comunidad': self.comunidad,
		}
		preoperaciones = PreOperacionesModelSerializer(queryset, context=context, many=True)
		return Response(preoperaciones.data)

