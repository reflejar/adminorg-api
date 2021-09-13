# Django
from django.db import models

# Custom
from adminsmart.utils.models import BaseModel

class PDF(BaseModel):
    """
        Modelo para almacenar los textos de los pdfs
        Cada vez que se solicita un pdf se genera de nuevo a traves del hash
        deberian eliminarse todas las noches
    """

    hash = models.CharField(max_length=512)
    location = models.FileField(upload_to="pdfs/", blank=True, null=True)

    def make_pdf(self, html_location, context):
        pass

    def serve(self):
        """TODO: si no se abre el pdf hay que volver a hacer y retornar"""

        return self.location