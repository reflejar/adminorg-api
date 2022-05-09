from django.contrib import admin
from adminsmart.apps.core.models import Comprobante


class ComprobanteAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"receipt_type",
		"point_of_sales",
		"issued_date",
	)

admin.site.register(Comprobante, ComprobanteAdmin)