from django.contrib import admin
from core.models import Operacion
from import_export.admin import ImportExportMixin


class OperacionAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['cuenta', 'comprobante', 'valor', 'total_pesos']
	list_filter = ['comunidad', 'cuenta__naturaleza']

admin.site.register(Operacion, OperacionAdmin)
