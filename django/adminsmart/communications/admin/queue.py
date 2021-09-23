from django.contrib import admin
from ..models import Queue


class QueueAdmin(admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['comunidad']

admin.site.register(Queue, QueueAdmin)
