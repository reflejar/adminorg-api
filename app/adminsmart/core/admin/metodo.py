from django.contrib import admin
from adminsmart.core.models import Metodo


class MetodoAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['comunidad']

admin.site.register(Metodo, MetodoAdmin)