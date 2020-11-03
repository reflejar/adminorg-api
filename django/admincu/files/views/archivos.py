
from admincu.utils.generics import custom_viewsets
from django.shortcuts import get_object_or_404 
from rest_framework import serializers
from django.db import transaction
from rest_framework.parsers import (
	JSONParser,
	FormParser,
	MultiPartParser
)

from admincu.files.models import Archivo
from admincu.files.serializers import ArchivoModelSerializer

class ArchivoViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Documentos recibidos de Proveedores View Set.
			Todos los tipos de documento
		Crea, actualiza, detalla y lista Documentos.
	"""

	parser_classes = [JSONParser, FormParser, MultiPartParser]
	serializer_class = ArchivoModelSerializer


	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj

	def get_queryset(self):
		try:
			return Archivo.objects.filter(comunidad=self.comunidad)
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