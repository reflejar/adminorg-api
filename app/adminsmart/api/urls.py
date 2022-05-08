from django.urls import include, path

urlpatterns = [

	# API
	path('files/', include(('adminsmart.api.files.urls', 'files'), namespace='files')),
	path('users/', include(('adminsmart.api.users.urls', 'users'), namespace='users')),
	path('utils/', include(('adminsmart.api.utils.urls', 'utils'), namespace='utils')),
	path('operative/', include(('adminsmart.api.core.urls', 'operative'), namespace='operative')),
	path('informes/', include(('adminsmart.api.informes.urls', 'informes'), namespace='informes')),
	path('public/', include(('adminsmart.api._public.urls', 'api'), namespace='api')),



]
