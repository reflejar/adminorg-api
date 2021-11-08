from django.contrib import admin
from django.contrib import messages
from adminsmart.operative.models import Documento, Operacion
from import_export.admin import ImportExportMixin
from adminsmart.operative.serializers.documentos.cliente import DestinoClienteModelSerializer

# from adminsmart.communications.tasks import send_emails

def hacer_pdf(modeladmin, request, queryset):
	for d in queryset:
		d.hacer_pdf()
	messages.add_message(request, messages.SUCCESS, "Hecho.")
hacer_pdf.short_description = "Hacer PDF"

def send_email(modeladmin, request, queryset):
	for d in queryset:
		documento = DestinoClienteModelSerializer(instance=d)
		documento.send_email(d)
	messages.add_message(request, messages.SUCCESS, "Hecho.")
send_email.short_description = "Enviar por mail"


def hard_delete(modeladmin, request, queryset):
	for documento in queryset:
		documento.operaciones.all().hard_delete()
		receipt = documento.receipt
		documento.hard_delete()
		receipt.delete()
		messages.add_message(request, messages.SUCCESS, "Hecho.")
hard_delete.short_description = "Hard delete"

class OperacionInline(admin.TabularInline):
	model = Operacion

class DocumentoAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['receipt', 'destinatario']
	list_filter = ['comunidad', 'receipt__receipt_type']
	actions = [hacer_pdf, send_email, hard_delete]
	inlines = [
		OperacionInline,
	]	

admin.site.register(Documento, DocumentoAdmin)