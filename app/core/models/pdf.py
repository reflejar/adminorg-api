import json
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
from utils.models import BaseModel

class PDF(BaseModel):
	"""
		Modelo para almacenar los textos de los pdfs
		Cada vez que se solicita un pdf se genera de nuevo a traves template y el context
		deberian eliminarse todas las noches
	"""

	ciphertext = models.BinaryField(blank=True, null=True) # Deprected
	context = models.TextField(blank=True, null=True)
	template = models.CharField(max_length=300, blank=True, null=True)
	location = models.FileField(upload_to="pdfs/", blank=True, null=True)

	@property
	def path(self):
		return self.serve().path

	def read(self):
		return self.serve().read()		

	@classmethod
	def compress(cls, html_location, context): # Deprected
		html_string = render_to_string(html_location, context)
		return zlib.compress(html_string.encode('utf-8'))

	def serve(self):
		if not self.location:
			pdf = self.prepare_pages().write_pdf()
			file_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(30)]) + ".pdf"
			self.location = SimpleUploadedFile(file_name, pdf, content_type='application/pdf')
			self.save()
		return self.location

	def prepare_pages(self):
		file = []
		completed = []
		# html_string = zlib.decompress(self.ciphertext)
		context = {'pdf': json.loads(self.context)}
		html_string = render_to_string(self.template, context)
		html = HTML(string=html_string, base_url='http://localhost:8000/')
		pdf = html.render()
		completed.append(pdf)
		for p in pdf.pages:
			file.append(p)
		return completed[0].copy(file)


	def remove(self):
		self.location.delete(False)
		self.location = None
		self.save()
