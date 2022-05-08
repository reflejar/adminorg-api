"""PublicAPI app."""

# Django
from django.apps import AppConfig


class PublicAPIAppConfig(AppConfig):
    """PublicAPI app config."""

    name = 'adminsmart.api._public'
    verbose_name = 'PublicAPI'
