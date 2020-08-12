from django.http import Http404
from rest_framework.permissions import IsAuthenticated

from admincu.users.permissions import IsAccountOwner, IsComunidadMember, IsAdministrativoUser
from admincu.utils.generics import custom_viewsets
from admincu.operative.serializers import CobroPlataformaModelSerializer

from admincu.operative.models import (
	Cobro
)

from admincu.operative.filters import CobroPlataformaFilter


class PlataformasViewSet(custom_viewsets.CustomModelViewSet):
	'''
	Parametros View Set.
	Crea Preferences de MP y lista los diferentes cobros de las plataformas.
	'''

	serializer_class = CobroPlataformaModelSerializer
	http_method_names = ['get', 'post']
	filterset_class = CobroPlataformaFilter

	def get_queryset(self):
		print(self.kwargs.keys())
		'''Define el queryset segun parametro de url.'''
		query = {
			'comunidad': self.comunidad,
			'documento__isnull': True
		}
		if 'plataforma' in self.kwargs.keys():
			query.update({
				'plataforma__platform_code': self.kwargs['platform_code']
			})

		try:
			queryset = Cobro.objects.filter(**query)
			return queryset
		except:
			raise Http404


	def get_permissions(self):
		'''Manejo de permisos'''
		permissions = [IsAuthenticated, IsAdministrativoUser]
		return [p() for p in permissions]


	# def get_serializer_context(self):
	# 	'''Agregado de naturaleza 'cliente' al context serializer.'''
	# 	serializer_context = super().get_serializer_context()
	# 	serializer_context['naturaleza'] = self.kwargs['naturaleza']
	# 	return serializer_context
