from django.contrib import admin
from admincu.operative.models import Metodo


class MetodoAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(Metodo, MetodoAdmin)