from django.http import Http404
from django.shortcuts import get_object_or_404 
from django.db import transaction

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from adminsmart.apps.users.permissions import IsComunidadMember, IsAdministrativoUser
from adminsmart.apps.utils.generics import custom_viewsets
from adminsmart.apps.core.models import PreOperacion
from adminsmart.api.core.serializers.importacion import ImportacionModelSerializer

class ImportacionViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Para la carga de preconceptos
		Utiliza el serializer con 
			many=True si es POST
			many=False si es UPDATE
	"""

	serializer_class = ImportacionModelSerializer

	def get_queryset(self):
		try:
			return PreOperacion.objects.filter(comunidad=self.comunidad)
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

	def list(self, request):
		preoperaciones = ImportacionModelSerializer(self.get_queryset(), context={'comunidad': self.comunidad}, many=True)
		return Response(preoperaciones.data)

