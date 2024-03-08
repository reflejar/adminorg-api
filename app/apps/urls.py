from django.urls import include, path

urlpatterns = [

	# API
	path('files/', include(('apps.files.urls', 'files'), namespace='files')),
	path('users/', include(('apps.users.urls', 'users'), namespace='users')),
	path('utils/', include(('apps.utils.urls', 'utils'), namespace='utils')),
	path('operative/', include(('apps.core.urls', 'operative'), namespace='operative')),
	path('reportes/', include(('apps.reportes.urls', 'reportes'), namespace='reportes')),

]
