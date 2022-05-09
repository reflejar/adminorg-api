from django.urls import include, path

from .index import index
from .modules.clientes import *

urlpatterns = [


	# Custom Views
    path('', index, name='index'),
	path('home/', ClientesView.as_view(), name='home'),
	path('cuentas-a-cobrar/', ClientesView.as_view(), name='clientes'),
	path('cuentas-a-pagar/', ClientesView.as_view(), name='proveedores'),
	path('tesoreria/', ClientesView.as_view(), name='tesoreria'),
	path('contabilidad/', ClientesView.as_view(), name='contabilidad'),
	path('informes/', ClientesView.as_view(), name='informes'),
	path('configuracion/', ClientesView.as_view(), name='configuracion'),

]
