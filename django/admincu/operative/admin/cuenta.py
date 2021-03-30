from django.contrib import admin
from admincu.operative.models import Cuenta, DefinicionVinculo
from import_export.admin import ImportExportMixin


class CuentaAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['comunidad', 'naturaleza']

admin.site.register(Cuenta, CuentaAdmin)

class DefinicionVinculoAdmin(admin.ModelAdmin):
	list_display = ['cuenta', 'cuenta_vinculada']

admin.site.register(DefinicionVinculo, DefinicionVinculoAdmin)