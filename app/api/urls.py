from django.urls import include, path

urlpatterns = [

	# API
	path('files/', include(('api.files.urls', 'files'), namespace='files')),
	path('users/', include(('api.users.urls', 'users'), namespace='users')),
	path('utils/', include(('api.utils.urls', 'utils'), namespace='utils')),
	path('operative/', include(('api.core.urls', 'operative'), namespace='operative')),
	path('informes/', include(('api.informes.urls', 'informes'), namespace='informes')),
	path('public/', include(('api._public.urls', 'api'), namespace='api')),



]
