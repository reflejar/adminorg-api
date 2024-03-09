from django.contrib import admin
from core.models import Cuenta
from import_export.admin import ImportExportMixin
from django.contrib import messages




class CuentaAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['comunidad', 'naturaleza']


admin.site.register(Cuenta, CuentaAdmin)

