from django.contrib import admin
from django.contrib import messages
from admincu.operative.models import Documento, Operacion

def hacer_pdf(modeladmin, request, queryset):
	for documento in queryset:
		documento.hacer_pdf()
		messages.add_message(request, messages.SUCCESS, "Hecho.")
hacer_pdf.short_description = "Hacer PDF"

class OperacionInline(admin.TabularInline):
	model = Operacion

class DocumentoAdmin(admin.ModelAdmin):
	list_display = ['receipt', 'destinatario']
	list_filter = ['comunidad', 'receipt__receipt_type']
	actions = [hacer_pdf]
	inlines = [
		OperacionInline,
	]	

admin.site.register(Documento, DocumentoAdmin)