from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from adminsmart.api.utils.serializers import ComunidadModelSerializer
from adminsmart.apps.utils.models import Comunidad
from adminsmart.apps.users.permissions import IsAdministrativoUser

class ComunidadViewSet(viewsets.ModelViewSet):
    '''Comunidad view set.'''

    queryset = Comunidad.objects.all()
    serializer_class = ComunidadModelSerializer

    def get_permissions(self):
        '''Asigna permisos basandose en la accion'''
        if self.action == 'list':
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated, IsAdministrativoUser]
        return [p() for p in permissions]