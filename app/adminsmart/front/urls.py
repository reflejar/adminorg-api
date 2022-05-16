from django.urls import include, path

from .modules.base import BlankView
from . import views

urlpatterns = [

	# Front door
    path('', views.index, name='index'),

	# Generic Views
	path('pdf/<int:pk>/', views.PDFViewer.as_view(), name='pdf-viewer'),

	# System App Views
	path('home/', BlankView.as_view(), name='home'),
	path('cuentas-a-cobrar/', include(
		('adminsmart.front.modules.clientes.urls', 'clientes'), namespace='clientes')
	),
	path('cuentas-a-pagar/', BlankView.as_view(), name='proveedores'),
	path('tesoreria/', BlankView.as_view(), name='tesoreria'),
	path('contabilidad/', BlankView.as_view(), name='contabilidad'),
	path('informes/', BlankView.as_view(), name='informes'),
	path('configuracion/', include(
		('adminsmart.front.modules.configuracion.urls', 'configuracion'), namespace='configuracion')
	),

	# Others
	path('perfil/', BlankView.as_view(), name='perfil'),
	path('biblioteca/', BlankView.as_view(), name='biblioteca'),

]
