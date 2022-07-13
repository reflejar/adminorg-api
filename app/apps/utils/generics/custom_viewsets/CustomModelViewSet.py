from rest_framework import viewsets
from django.core.paginator import Paginator

from apps.utils.models import Comunidad


class CustomModelViewSet(viewsets.ModelViewSet):
	'''Model View Set custom'''

	http_method_names = ['get', 'post', 'put', 'options', 'delete'] # Define los metodos aceptados por la vista. Se anula update partial.

	def initial(self, request, *args, **kwargs):
		'''Obtiene comunidad desde request volverla siempre disponible'''
		super().initial(request, *args, **kwargs)
		self.comunidad = request.user.perfil_set.first().comunidad

	def get_serializer_context(self):
		"""Extra contexto provisto al serilizer. Agrega comunidad."""
		return {
			'request': self.request,
			'format': self.format_kwarg,
			'view': self,
			'comunidad': self.comunidad
		}
