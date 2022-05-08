
from adminsmart.utils.generics import custom_viewsets
from django.shortcuts import get_object_or_404 
from rest_framework import serializers
from django.db import transaction

from adminsmart.files.models import Carpeta
from adminsmart.api.files.serializers import CarpetaModelSerializer

class CarpetaViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Documentos recibidos de Proveedores View Set.
			Todos los tipos de documento
		Crea, actualiza, detalla y lista Documentos.
	"""

	serializer_class = CarpetaModelSerializer

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj

	def get_queryset(self):
		try:
			return Carpeta.objects.filter(comunidad=self.comunidad)
		except:
			raise Http404


	@transaction.atomic
	def update(self, request, *args, **kwargs):

		obj = self.get_object()

		return super().update(request, *args, **kwargs)

	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		"""
			Para ELIMINAR una carpeta
			Se establece una validacion en la cual
				NO SE PUEDE ELIMINAR SI TIENE ARCHIVOS O CARPETAS DENTRO
		"""
		
		obj = self.get_object()
	
		raise serializers.ValidationError("Debe eliminar o mover los archivos que esta carpeta contiene")
		
		return Response(status=status.HTTP_204_NO_CONTENT)			