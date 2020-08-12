from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from admincu.utils.models import (
    Comunidad,
    Domicilio,
    TipoComunidad,
    Provincia
)


class ComunidadAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(Comunidad, ComunidadAdmin)


class TipoComunidadAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(TipoComunidad, TipoComunidadAdmin)


class DomicilioAdmin(admin.ModelAdmin):
	list_display = ['calle']
	list_filter = ['calle']

admin.site.register(Domicilio, DomicilioAdmin)


class ProvinciaAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(Provincia, ProvinciaAdmin)
