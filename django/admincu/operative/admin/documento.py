from django.contrib import admin
from django.contrib import messages
from admincu.operative.models import Documento, Operacion
from import_export.admin import ImportExportMixin

from admincu.taskapp.tasks import hacer_pdfs, enviar_mails

def hacer_pdf(modeladmin, request, queryset):
	hacer_pdfs.delay([d.id for d in queryset])
	messages.add_message(request, messages.SUCCESS, "Hecho.")
hacer_pdf.short_description = "Hacer PDF"

def enviar_mail(modeladmin, request, queryset):
	enviar_mails.delay([d.id for d in queryset])
	messages.add_message(request, messages.SUCCESS, "Hecho.")
enviar_mail.short_description = "Enviar por mail"


def hard_delete(modeladmin, request, queryset):
	for documento in queryset:
		for op in documento.operaciones.all():
			op.metodos.all().hard_delete()
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
	actions = [hacer_pdf, enviar_mail, hard_delete]
	inlines = [
		OperacionInline,
	]	

admin.site.register(Documento, DocumentoAdmin)