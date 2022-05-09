from django.db import models
from adminsmart.apps.utils.models import BaseModel
from adminsmart.apps.core.models import Documento

# class CuentaEP(models.Model):

# 	nombre = models.CharField(max_length=50)
# 	app_code = models.PositiveIntegerField(blank=True, null=True)
# 	app_di = models.PositiveIntegerField(blank=True, null=True)

# 	def __str__(self):
# 		return self.nombre


# class CuponEP(models.Model):

# 	""" Agrega datos de exp necesarios al dcocumento."""

# 	documento = models.ForeignKey(Documento, related_name='preferences_ep', on_delete=models.CASCADE)
# 	barcode = models.CharField(max_length=90)
# 	cpe = models.CharField(max_length=6516)
# 	inf_deuda = models.BooleanField(default=False)
# 	pdf = models.FileField(upload_to="pdfs/expensas_pagas/", blank=True, null=True)

# class CobroEP(models.Model):

# 	""" Cobros Expensas Pagas Model."""

# 	codigo_consorcio = models.PositiveIntegerField(blank=True, null=True)
# 	unidad_funcional = models.PositiveIntegerField(blank=True, null=True)
# 	fecha_cobro = models.DateField(blank=True, null=True)
# 	importe_cobrado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
# 	comision_plataforma = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
# 	neto_a_depositar = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
# 	canal_de_pago = models.CharField(max_length=15)
