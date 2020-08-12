from django.contrib import admin
from admincu.operative.models import Cuenta, DefinicionVinculo


class CuentaAdmin(admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['naturaleza', 'comunidad']

admin.site.register(Cuenta, CuentaAdmin)

class DefinicionVinculoAdmin(admin.ModelAdmin):
	list_display = ['cuenta', 'cuenta_vinculada']

admin.site.register(DefinicionVinculo, DefinicionVinculoAdmin)