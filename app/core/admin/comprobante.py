from django.contrib import admin
from django.contrib import messages
from core.models import Comprobante, Operacion
from import_export.admin import ImportExportMixin
# from core.serializers.comprobantes.cliente import DestinoClienteModelSerializer

# from communications.tasks import send_emails

def hacer_pdf(modeladmin, request, queryset):
	for d in queryset:
		d.hacer_pdf()
	messages.add_message(request, messages.SUCCESS, "Hecho.")
hacer_pdf.short_description = "Hacer PDF"


def hard_delete(modeladmin, request, queryset):
	for comprobante in queryset:
		comprobante.operaciones.all().hard_delete()
		receipt = comprobante.receipt
		comprobante.hard_delete()
		receipt.delete()
		messages.add_message(request, messages.SUCCESS, "Hecho.")
hard_delete.short_description = "Hard delete"

class OperacionInline(admin.TabularInline):
	model = Operacion

class ComprobanteAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['receipt', 'destinatario']
	list_filter = ['comunidad', 'receipt__receipt_type']
	actions = [
		hacer_pdf, 
		# send_email, 
		hard_delete
		]
	inlines = [
		OperacionInline,
	]	

admin.site.register(Comprobante, ComprobanteAdmin)