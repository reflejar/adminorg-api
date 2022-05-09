from django.contrib import admin
from adminsmart.apps.files.models import PDF

class PDFAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'comunidad']
	list_filter = ['comunidad']

admin.site.register(PDF, PDFAdmin)