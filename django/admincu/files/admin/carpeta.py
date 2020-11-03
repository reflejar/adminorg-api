from django.contrib import admin
from admincu.files.models import Carpeta

class CarpetaAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'comunidad']
	list_filter = ['comunidad']

admin.site.register(Carpeta, CarpetaAdmin)