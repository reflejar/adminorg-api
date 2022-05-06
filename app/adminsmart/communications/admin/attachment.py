from django.contrib import admin
from ..models import Attachment


class AttachmentAdmin(admin.ModelAdmin):
	list_display = ['__str__',]
	
admin.site.register(Attachment, AttachmentAdmin)
