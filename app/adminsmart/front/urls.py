from django.urls import include, path

from .index import index
from .modules.clientes.views import IndexView as ClientesView

urlpatterns = [

	# Front door
    path('', index, name='index'),
	path('home/', ClientesView.as_view(), name='home'),
	path('cuentas-a-cobrar/', include(
		('adminsmart.front.modules.clientes.urls', 'clientes'), namespace='clientes')
	),
	path('cuentas-a-pagar/', ClientesView.as_view(), name='proveedores'),
	path('tesoreria/', ClientesView.as_view(), name='tesoreria'),
	path('contabilidad/', ClientesView.as_view(), name='contabilidad'),
	path('informes/', ClientesView.as_view(), name='informes'),
	path('configuracion/', include(
		('adminsmart.front.modules.configuracion.urls', 'configuracion'), namespace='configuracion')
	),

]
