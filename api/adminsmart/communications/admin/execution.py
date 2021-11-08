from django.contrib import admin
from ..models import Execution


class ExecutionAdmin(admin.ModelAdmin):
	list_display = ['__str__']
	list_filter = ['comunidad']

admin.site.register(Execution, ExecutionAdmin)
