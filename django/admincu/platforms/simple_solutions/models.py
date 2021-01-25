from admincu.utils.models import BaseModel



# class Account(BaseModel):

# 	nombre = models.CharField(max_length=100)
# 	carpeta = models.CharField(max_length=100)

# 	def __str__(self):
# 		return self.nombre



# class Sent(BaseModel):

# 	"""
# 		BaseModel ya tiene un fecha_creacion asi que no hace falta agregarle la fecha de envio
# 	"""

# 	documento = models.ForeignKey(Documento, related_name='envio_ss', on_delete=models.CASCADE)
# 	observacion = models.TextField(blank=True, null=True) # Por ahora no se usa. Hecho para captar el hipotetico error y colocar el texto aqui

# 	def __str__(self):
# 		return str(self.documento)
