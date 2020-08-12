"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from admincu.users.models import User
from admincu.users.models import Perfil


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', )
    list_filter = ('is_staff',)

admin.site.register(User, CustomUserAdmin)

class PerfilAdmin(admin.ModelAdmin):
	list_display = ['nombre']
	list_filter = ['nombre']

admin.site.register(Perfil, PerfilAdmin)
