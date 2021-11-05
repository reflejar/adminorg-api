from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from adminsmart.utils.models import (
    Comunidad,
    Domicilio,
    TipoComunidad,
    Provincia
)

from adminsmart.operative.models import (
	Operacion,
	Documento,
	Titulo
)

from django_afip.models import Receipt

def borrar_data(modeladmin, request, queryset):
	Operacion.all_objects.filter(comunidad__in=queryset).hard_delete()
	Documento.all_objects.filter(comunidad__in=queryset).hard_delete()
	Receipt.objects.all().delete()
	

borrar_data.short_description = "Borrar toda la data operativa excepto las cuentas"

def crear_plan_basico(modeladmin, request, queryset):
	for comunidad in queryset:
		
		activo = Titulo.objects.create(
			comunidad=comunidad,
			nombre="ACTIVO",
			numero=100000,
			supertitulo=None
		)
		pasivo = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PASIVO",
			numero=200000,
			supertitulo=None
		)		
		patrimonio_neto = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PATRIMONIO NETO",
			numero=300000,
			supertitulo=None
		)		
		recursos = Titulo.objects.create(
			comunidad=comunidad,
			nombre="RECURSOS",
			numero=400000,
			supertitulo=None
		)
		gastos = Titulo.objects.create(
			comunidad=comunidad,
			nombre="GASTOS",
			numero=500000,
			supertitulo=None
		)		
		caja = Titulo.objects.create(
			comunidad=comunidad,
			nombre="TESORERIA",
			numero=111101,
			supertitulo=activo
		)					
		cuentas_a_cobrar = Titulo.objects.create(
			comunidad=comunidad,
			nombre="CUENTAS A COBRAR",
			numero=112101,
			supertitulo=activo
		)	
		bienes_de_cambio = Titulo.objects.create(
			comunidad=comunidad,
			nombre="BIENES DE CAMBIO",
			numero=113101,
			supertitulo=activo
		)				
		cuentas_a_pagar = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PROVEEDORES",
			numero=211101,
			supertitulo=pasivo
		)		

crear_plan_basico.short_description = "Crear plan de cuentas basico"


class ComunidadAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']
	actions = [
		borrar_data,
		crear_plan_basico
	]

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
