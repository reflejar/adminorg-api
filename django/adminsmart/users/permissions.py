"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same."""
        return request.user in obj.perfil.users.all()


class IsAdministrativoUser(BasePermission):
    '''Allow acces only administrativo user'''

    def has_permission(self, request, view):
        return request.user.groups.all()[0].name == 'administrativo'
    
class IsComunidadMember(BasePermission):
    """Permite acceso solo a usuarios de la comunidad."""

    def has_object_permission(self, request, view, obj):
        """Check obj comunidad and user comunidad are the same."""
        return request.user.perfil_set.first().comunidad == obj.comunidad

class IsSocioUser(BasePermission):
    '''Allow acces only socio user'''

    def has_permission(self, request, view):
        return request.user.groups.all()[0].name == 'socio'
    
class IsPlatformClientUser(BasePermission):
    '''Allow acces only platform client user'''

    def has_permission(self, request, view):
        return request.user.groups.all()[0].name == 'plataforma'