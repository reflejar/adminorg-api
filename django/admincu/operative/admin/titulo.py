from django.contrib import admin
from admincu.operative.models import Titulo
from import_export.admin import ImportExportMixin


class TituloAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['comunidad']

admin.site.register(Titulo, TituloAdmin)