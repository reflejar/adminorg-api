from django.contrib import admin
from adminsmart.core.models import Cuenta, DefinicionVinculo
from import_export.admin import ImportExportMixin
from django.contrib import messages







def makeJSON(d, cuenta):
	'''copia aproximada del makeJSON de serializer estado de cuenta'''
	saldo = 0 #esto no es 0 en la vida real sino que viene con valor
	

	receipt_type = str(d.receipt.receipt_type)
	formatted_number = str(d.receipt.formatted_number)
	operaciones=[]
	total = 0
	for o in d.operaciones.all():
		if o.cuenta in cuenta.grupo:
			operaciones.append(o)
			total += o.valor
	saldo += total

	return {
		'id': d.id,
		'fecha': d.fecha_operacion,
		'causante': d.causante,
		'fecha_anulacion': d.fecha_anulacion,
		'nombre': receipt_type + " " + formatted_number,
		'receipt': {
			'receipt_type': receipt_type,
			'formatted_number': formatted_number,
		},
		'operaciones': [{
			'cuenta': str(o.cuenta),
			'concepto': str(o.concepto()),
			'periodo': o.periodo(),
			'valor': o.valor,
		} for o in operaciones],
		'total': total,
		'saldo':saldo
	}


def documentos_estado_de_cuenta(modeladmin, request, queryset):
	for c in queryset:
		r = c.estado_cuenta()
		if request:
			messages.add_message(request, messages.SUCCESS, str(r))
	return r	

documentos_estado_de_cuenta.short_description = "documentos estado de cuenta"


def serializer_nuevo(modeladmin, request, queryset):
		r = documentos_estado_de_cuenta(queryset=queryset, modeladmin=None, request=None)
		cuenta = queryset.first()
		for d in r:
			f = makeJSON(d, cuenta)  #la forma mas sencilla es hacerle llegar la cuenta al makeJSON, eso va aqui queryser, eso hay que ver como hacerlo en la version real, failita mucho el trabajo porque no hay que hacer mas retoques, no se puede ir a buscarla desde el documento porque hay documentos que no tienen cuentas
			messages.add_message(request, messages.SUCCESS, f)

serializer_nuevo.short_description = "serializer estado de cuenta"







class CuentaAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['comunidad', 'naturaleza']
	actions = [
		documentos_estado_de_cuenta,
		serializer_nuevo,
	]


admin.site.register(Cuenta, CuentaAdmin)

class DefinicionVinculoAdmin(admin.ModelAdmin):
	list_display = ['cuenta', 'cuenta_vinculada']

admin.site.register(DefinicionVinculo, DefinicionVinculoAdmin)