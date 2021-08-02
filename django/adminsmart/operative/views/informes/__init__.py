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
from adminsmart.users.permissions import IsComunidadMember, IsAdministrativoUser
from adminsmart.utils.generics import custom_viewsets
from adminsmart.operative.models import (
	Operacion
)
from adminsmart.operative.serializers.informes import InformesModelSerializer
from adminsmart.operative.filters import InformesFilter

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
			datos = Operacion.objects.filter(
				comunidad=self.comunidad,
				documento__isnull=False
			).select_related(
				"cuenta", 
				"cuenta__perfil", # Para el nombre de la cuenta
				"cuenta__titulo", 
				"cuenta__naturaleza",
				"documento__receipt", 
				"documento__receipt__receipt_type", 
				"vinculo",
			).prefetch_related(
				"vinculos",
				"vinculos__cuenta",
				"vinculos__cuenta__naturaleza",
				"vinculo__vinculos",
				"vinculo__vinculos__cuenta",
				"vinculo__vinculos__cuenta__naturaleza",
			)
			self.filter = self.filterset_class(self.request.GET, queryset=datos)
			return self.filter.qs
		except:
			raise Http404

	def get_serializer_context(self):
		'''Agregado de naturaleza 'cliente' al context serializer.'''
		serializer_context = super().get_serializer_context()
		end_date = datetime.strptime(self.request.GET['end_date'], "%Y-%m-%d").date()
		serializer_context['end_date'] = end_date
		return serializer_context

	def list(self, request):
		queryset = self.get_queryset()

		# operaciones = self.serializer_class(queryset, many=True)
		data = [InformesModelSerializer(o) for o in queryset]
		return Response(data)
		# return Response(operaciones.data)



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

