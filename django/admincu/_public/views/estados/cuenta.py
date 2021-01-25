from django.shortcuts import get_object_or_404 
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from admincu.operative.models import Cuenta
from admincu.users.permissions import IsPlatformClientUser
from admincu._public.serializers import EstadoCuentaModelSerializer

class EstadoCuentaViewSet(viewsets.ModelViewSet):
	'''Estado de cuenta de un socio view set.'''

	serializer_class = EstadoCuentaModelSerializer
	http_method_names = ['get']

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj


	def get_queryset(self):
		try:
			kwargs = {
				'naturaleza__nombre': "cliente",
			}
			return Cuenta.objects.filter(**kwargs)
		except:
			raise Http404    

	def get_permissions(self):
		'''Asigna permisos basandose en la accion'''
		permissions = [IsAuthenticated, IsPlatformClientUser]
		return [p() for p in permissions]