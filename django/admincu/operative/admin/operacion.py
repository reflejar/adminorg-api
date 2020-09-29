from django.contrib import admin
from admincu.operative.models import Operacion


class OperacionAdmin(admin.ModelAdmin):
	list_display = ['cuenta', 'valor']
	list_filter = ['comunidad']

admin.site.register(Operacion, OperacionAdmin)
