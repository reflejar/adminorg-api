import random
import string
import zlib
from weasyprint import HTML

# Django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template.loader import render_to_string
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_delete

# Custom
from adminsmart.utils.models import BaseModel

class PDF(BaseModel):
	"""
		Modelo para almacenar los textos de los pdfs
		Cada vez que se solicita un pdf se genera de nuevo a traves del ciphertext
		deberian eliminarse todas las noches
	"""

	ciphertext = models.BinaryField(blank=True, null=True)
	location = models.FileField(upload_to="pdfs/", blank=True, null=True)

	@classmethod
	def compress(cls, html_location, context):
		html_string = render_to_string(html_location, context)
		return zlib.compress(html_string.encode('utf-8'))

	def serve(self):
		if not self.location:
			file = []
			completed = []
			html_string = zlib.decompress(self.ciphertext)
			html = HTML(string=html_string, base_url='http://localhost:8000/')
			pdf = html.render()
			completed.append(pdf)
			for p in pdf.pages:
				file.append(p)

			pdf = completed[0].copy(file).write_pdf()			
			file_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(30)]) + ".pdf"
			self.location = SimpleUploadedFile(file_name, pdf, content_type='application/pdf')
			self.save()
		return self.location
	
	def remove(self):
		self.location.delete(False)
		self.location = None
		self.save()