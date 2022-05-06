from django.contrib import admin
from ..models import Queue
from django.contrib import messages

def exec_send(modeladmin, request, queryset):
	for d in queryset:
		d.exec()
	messages.add_message(request, messages.SUCCESS, "Hecho.")
exec_send.short_description = "Ejecutar envio"

class QueueAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'addressee', 'observations', 'client', 'execute_at', 'tried']
	list_filter = ['comunidad', 'client']
	actions = [exec_send]
	
admin.site.register(Queue, QueueAdmin)
