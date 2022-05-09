from django.contrib import admin
from adminsmart.apps.core.models import PreOperacion
from import_export.admin import ImportExportMixin


class PreOperacionAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['cuenta', 'valor']
	list_filter = ['comunidad', 'cuenta__naturaleza']

admin.site.register(PreOperacion, PreOperacionAdmin)
