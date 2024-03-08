from django.contrib import admin
from core.models import Naturaleza


class NaturalezaAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(Naturaleza, NaturalezaAdmin)