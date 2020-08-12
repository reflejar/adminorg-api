from django.contrib import admin
from .models import Plataforma


class PlataformaAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'comunidad']
	list_filter = ['comunidad']

admin.site.register(Plataforma, PlataformaAdmin)