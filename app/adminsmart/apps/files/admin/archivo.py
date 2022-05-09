from django.contrib import admin
from adminsmart.apps.files.models import Archivo


class ArchivoAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'comunidad']
	list_filter = ['comunidad']

admin.site.register(Archivo, ArchivoAdmin)