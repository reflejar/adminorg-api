from django.db import models
from adminsmart.utils.models import BaseModel


# class CuentaSS(BaseModel):

# 	nombre = models.CharField(max_length=100)
# 	carpeta = models.CharField(max_length=100)

# 	def __str__(self):
# 		return self.nombre


# class EnvioSS(BaseModel):

# 	"""
# 		BaseModel ya tiene un fecha_creacion asi que no hace falta agregarle la fecha de envio
# 	"""

# 	modelo = models.CharField(max_length=20)
# 	id_modelo = models.PositiveIntegerField()
# 	filtros = models.CharField(max_length=100) # Se utiliza actualmente para filtrar en el modelo Documento, que tiene diferentes tipos de documento
# 	observacion = models.TextField(blank=True, null=True) # Por ahora no se usa. Hecho para captar el hipotetico error y colocar el texto aqui

# 	def __str__(self):
# 		return str(self.documento)
