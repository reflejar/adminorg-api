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

	context = models.TextField(blank=True, null=True)

	def serve(self):
		pdf = self.prepare_pages().write_pdf()
		return pdf

	def prepare_pages(self):
		file = []
		completed = []
		# html_string = zlib.decompress(self.ciphertext)
		context = {'pdf': json.loads(self.context)}
		html_string = render_to_string('pdfs/comprobante.html', context)
		html = HTML(string=html_string)
		pdf = html.render()
		completed.append(pdf)
		for p in pdf.pages:
			file.append(p)
		return completed[0].copy(file)
