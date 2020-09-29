from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from admincu.utils.models import (
    Comunidad,
    Domicilio,
    TipoComunidad,
    Provincia
)

from admincu.operative.models import (
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
		activo_corriente = Titulo.objects.create(
			comunidad=comunidad,
			nombre="ACTIVO CORRIENTE",
			numero=110000,
			supertitulo=activo
		)
		caja_y_bancos = Titulo.objects.create(
			comunidad=comunidad,
			nombre="CAJA Y BANCOS",
			numero=111000,
			supertitulo=activo_corriente
		)		
		caja = Titulo.objects.create(
			comunidad=comunidad,
			nombre="CAJA",
			numero=111101,
			supertitulo=caja_y_bancos
		)			
		banco = Titulo.objects.create(
			comunidad=comunidad,
			nombre="BANCO CUENTA CORRIENTE",
			numero=111102,
			supertitulo=caja_y_bancos
		)			
		creditos = Titulo.objects.create(
			comunidad=comunidad,
			nombre="CREDITOS",
			numero=112000,
			supertitulo=activo_corriente
		)		
		creditos_con_socios = Titulo.objects.create(
			comunidad=comunidad,
			nombre="CREDITOS CON SOCIOS",
			numero=112101,
			supertitulo=creditos
		)	
		bienes_de_cambio = Titulo.objects.create(
			comunidad=comunidad,
			nombre="BIENES DE CAMBIO",
			numero=113000,
			supertitulo=activo_corriente
		)				
		bienes_de_uso = Titulo.objects.create(
			comunidad=comunidad,
			nombre="BIENES DE USO",
			numero=114000,
			supertitulo=activo_corriente
		)				
		activo_no_corriente = Titulo.objects.create(
			comunidad=comunidad,
			nombre="ACTIVO NO CORRIENTE",
			numero=120000,
			supertitulo=activo
		)

		pasivo = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PASIVO",
			numero=200000,
			supertitulo=None
		)
		pasivo_corriente = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PASIVO CORRIENTE",
			numero=210000,
			supertitulo=pasivo
		)
		proveedores = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PROVEEDORES",
			numero=211000,
			supertitulo=pasivo_corriente
		)		
		pasivo_no_corriente = Titulo.objects.create(
			comunidad=comunidad,
			nombre="PASIVO NO CORRIENTE",
			numero=210000,
			supertitulo=pasivo
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
