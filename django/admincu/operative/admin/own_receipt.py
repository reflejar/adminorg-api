from django.contrib import admin
from django.contrib import messages
from import_export.admin import ImportExportMixin
from admincu.operative.models import OwnReceipt


class OwnReceiptAdmin(ImportExportMixin, admin.ModelAdmin):
	list_display = ['document_type', 'formatted_number', 'total_amount']
	list_filter = ['document_type']

admin.site.register(OwnReceipt, OwnReceiptAdmin)