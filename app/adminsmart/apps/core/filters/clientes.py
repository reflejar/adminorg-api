from adminsmart.apps.users.models import Perfil
from adminsmart.apps.core.models import Cuenta 
from django_filters.rest_framework import FilterSet, filters


class ClienteFilter(FilterSet):

    taxon__nombre = filters.CharFilter(lookup_expr="exact")
    perfil__nombre = filters.CharFilter(lookup_expr="icontains")
    perfil__apellido = filters.CharFilter(lookup_expr="icontains")
    perfil__razon_social = filters.CharFilter(lookup_expr="icontains")
    perfil__numero_documento = filters.NumberFilter(lookup_expr="exact")

    class Meta:
        model = Cuenta
        fields = []
