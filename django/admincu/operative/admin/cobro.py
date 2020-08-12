from django.contrib import admin
from admincu.operative.models import Cobro


class CobroAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'valor', 'comunidad']
	list_filter = ['comunidad']

admin.site.register(Cobro, CobroAdmin)