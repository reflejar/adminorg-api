"""Perfil model."""

# Django
from django.db import models
from django.core.validators import RegexValidator
from django_afip.models import DocumentType
# Utilities
from adminsmart.utils.models import BaseModel


class Perfil(BaseModel):
    """
		Modelo de perfil para cualquier persona (Fisica o Juridica), Cliente, Socio, Proveedores y para Lotes
	"""

    users = models.ManyToManyField('users.User', blank=True)

    nombre = models.CharField(max_length=80, blank=True, null=True)
    apellido = models.CharField(max_length=80, blank=True, null=True)
    razon_social = models.CharField(max_length=80, blank=True, null=True)
    tipo_documento = models.ForeignKey(DocumentType, blank=True, null=True, on_delete=models.SET_NULL)
    numero_documento = models.CharField(max_length=13)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    es_extranjero = models.BooleanField(default=False)
    mail = models.EmailField(blank=True, null=True, max_length=254)
    domicilio = models.ForeignKey("utils.Domicilio", blank=True, null=True, on_delete=models.SET_NULL)
    telefono_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    telefono = models.CharField(validators=[telefono_regex], max_length=17, blank=True)
    comunidades = models.ManyToManyField("utils.Comunidad", blank=True, related_name="admins")

    def __str__(self):
        nombre = ""
        nombre += "{} ".format(self.razon_social) if self.razon_social else ""
        nombre += "{} ".format(self.apellido) if self.apellido else ""
        nombre += "{}".format(self.nombre) if self.nombre else ""
        return nombre

    def get_emails_destinatarios(self):
        destinatarios = []
        [destinatarios.append(email) for email in [self.mail] + list(self.users.all().values_list('email', flat=True))
         if (email and not email in destinatarios)]
        return destinatarios
