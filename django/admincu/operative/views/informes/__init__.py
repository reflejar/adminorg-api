from django.http import Http404
from datetime import datetime
from django.shortcuts import get_object_or_404 
from django.db import transaction

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django_afip.models import (
	DocumentType,
	ReceiptType,
)
from admincu.users.permissions import IsComunidadMember, IsAdministrativoUser
from admincu.utils.generics import custom_viewsets
from admincu.operative.models import (
	Operacion
)
from admincu.operative.serializers.informes import InformesModelSerializer
from admincu.operative.filters import InformesFilter

class InformesViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Unicamente se hacen peticiones GET
		Es la vista para recopilar la data para hacer reportes y analisis
	"""

	http_method_names = ['get']
	serializer_class = InformesModelSerializer
	filterset_class = InformesFilter

	def get_queryset(self):
		try:
			return Operacion.objects.filter(
				comunidad=self.comunidad,
			)
		except:
			raise Http404

	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		end_date = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date()
		serializer_context['end_date'] = end_date
		return serializer_context

	# def get_object(self):
	# 	obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
	# 	self.check_object_permissions(self.request, obj)
	# 	return obj


	# def get_permissions(self):
	# 	'''Manejo de permisos'''
	# 	permissions = [IsAuthenticated, IsAdministrativoUser]
	# 	if self.action in ['update', 'retrieve', 'delete']:
	# 		permissions.append(IsComunidadMember)
	# 	return [p() for p in permissions]

	
	# def create(self, request, *args, **kwargs):
	# 	for r in request.data:
	# 		serializer = self.get_serializer(data=r)
	# 		serializer.is_valid(raise_exception=True)
	# 		self.perform_create(serializer)
	# 	return Response(status=status.HTTP_201_CREATED)


	# def list(self, request):
	# 	queryset = self.get_queryset()
	# 	context = {
	# 		'comunidad': self.comunidad,
	# 	}
	# 	operaciones = OperacionModelSerializer(queryset, context=context, many=True)
	# 	return Response(operaciones.data)

