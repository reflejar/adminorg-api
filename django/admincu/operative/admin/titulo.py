from django.contrib import admin
from admincu.operative.models import Titulo


class TituloAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['comunidad']

admin.site.register(Titulo, TituloAdmin)