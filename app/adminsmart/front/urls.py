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
	path('cuentas-a-pagar/', include(
		('adminsmart.front.modules.proveedores.urls', 'proveedores'), namespace='proveedores')
	),
	path('tesoreria/', include(
		('adminsmart.front.modules.tesoreria.urls', 'tesoreria'), namespace='tesoreria')
	),
	path('contabilidad/', include(
		('adminsmart.front.modules.contabilidad.urls', 'contabilidad'), namespace='contabilidad')
	),
	path('informes/', BlankView.as_view(), name='informes'),
	path('configuracion/', include(
		('adminsmart.front.modules.configuracion.urls', 'configuracion'), namespace='configuracion')
	),

	# Others
	path('perfil/', BlankView.as_view(), name='perfil'),
	path('biblioteca/', BlankView.as_view(), name='biblioteca'),

]
