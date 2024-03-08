from django.contrib import admin
from ..models import Execution


class ExecutionAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'addressee', 'observations', 'client', 'executed_at']
	list_filter = ['comunidad', 'client']

admin.site.register(Execution, ExecutionAdmin)
