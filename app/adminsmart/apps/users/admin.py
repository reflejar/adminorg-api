"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages

# Models
from adminsmart.apps.users.models import User
from adminsmart.apps.users.models import Perfil

def validar(modeladmin, request, queryset):
	for user in queryset:
		user.is_verified = True
		user.save()
	messages.add_message(request, messages.SUCCESS, "Validado.")

validar.short_description = "Validar el acceso al usuario"

class CustomUserAdmin(UserAdmin):
	"""User model admin."""

	list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', )
	list_filter = ('is_staff',)
	actions = [validar]

admin.site.register(User, CustomUserAdmin)


class PerfilAdmin(admin.ModelAdmin):
	list_display = ['id','apellido', 'nombre', 'razon_social', "tipo_documento", "numero_documento", "mail", "comunidad"]
	list_filter = ['comunidad']

admin.site.register(Perfil, PerfilAdmin)
