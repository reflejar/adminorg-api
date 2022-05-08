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
	# path('puntosdeventa/', arq_puntos, name='puntosdeventa'),
	# path('accesorios/<str:clase>/crear/', CrearAccesorio.as_view(), name='crear_accesorio'),
	# path('accesorios/<int:pk>/', FinalizarAccesorio.as_view(), name='finalizar_accesorio'), # Para finalizar un accesorio, descuento o interes
	# path('accesorios/<str:clase>/', ListadoAccesorio.as_view(), name='listado_accesorio'),
	# path('codigo/<int:pk>/', PDFCodigo.as_view(), name='codigo-socio'),

	# path('<str:modelo>/', Listado.as_view(), name='parametro'),
	# path('<str:modelo>/nuevo/', Crear.as_view(), name='crear'),
	# path('<str:modelo>/<int:pk>/editar/', Instancia.as_view(), name='instancia'),
	# path('<str:modelo>/<int:pk>/finalizar/', Finalizar.as_view(), name='finalizar-parametro'),
	# path('<str:modelo>/<int:pk>/reactivar/', Reactivar.as_view(), name='reactivar-parametro'),

]
