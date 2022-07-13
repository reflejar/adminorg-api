from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404 
from django.http import Http404

from apps.utils.generics import custom_viewsets
from apps.files.models import PDF

class PDFViewSet(custom_viewsets.CustomModelViewSet):
	"""
		Visualizacion de PDFs
	"""

	http_method_names = ['get']
	
	def retrieve(self, request, pk):
		response = HttpResponse(self.get_object().serve(), content_type='application/pdf')
		nombre = "%s.pdf" % "Hola"
		content = "inline; filename=%s" % nombre
		response['Content-Disposition'] = content
		return response

	def get_object(self):
		obj = get_object_or_404(PDF.objects.filter(comunidad=self.comunidad), pk=self.kwargs["pk"])
		self.check_object_permissions(self.request, obj)
		return obj
