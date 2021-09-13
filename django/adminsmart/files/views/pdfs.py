from django.shortcuts import get_object_or_404 
from django.http import Http404

from adminsmart.utils.generics import custom_viewsets
from adminsmart.files.models import PDF

class PDFViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Visualizacion de PDFs
	"""

	http_method_names = ['get'] 

	def get_object(self):
		obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj

	def get_queryset(self):
		try:
			return PDF.objects.filter(comunidad=self.comunidad)
		except:
			raise Http404