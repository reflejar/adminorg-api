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
from adminsmart.utils.models import BaseModel

class PDF(BaseModel):
	"""
		Modelo para almacenar los textos de los pdfs
		Cada vez que se solicita un pdf se genera de nuevo a traves del ciphertext
		deberian eliminarse todas las noches
	"""

	ciphertext = models.BinaryField(blank=True, null=True)
	location = models.FileField(upload_to="pdfs/", blank=True, null=True)

	@property
	def path(self):
		return self.serve().path

	def read(self):
		return self.serve().read()		

	@classmethod
	def compress(cls, html_location, context):
		html_string = render_to_string(html_location, context)
		return zlib.compress(html_string.encode('utf-8'))

	@classmethod
	def generate_content_fields(cls, doc):
		fields = {
			'cuenta': 'CUENTA',
			'concepto': 'CONCEPTO',
			'fecha_indicativa': 'PERIODO',
			'monto': 'MONTO',
			'detalle': "DETALLE",
			'vinculo.pdf.receipt.receipt_type': "DOC_TYPE_VINCULO",
			'vinculo.pdf.receipt.formatted_number': "DOC_NUM_VINCULO"
		}
		
		result = {
			'CREDITOS': [],
			'COBROS': [],
			'A_CUENTA': [],
			'PAGOS': [],
		}
		for key in result.keys():
			list_objects = []
			for op in getattr(doc, key.lower())():
				new_obj = {}
				for f in fields:
					dispatcher = getattr(op, f, None)
					if callable(dispatcher):
						dispatcher = dispatcher()
					new_obj[fields[f]] = str(dispatcher)
				list_objects.append(new_obj)
			result[key] = list_objects

		
		return json.dumps(result)
					
		# if doc.creditos():
		# 	objects['creditos'] = doc.creditos().values()
		# 	# objects['creditos'] = [{
		# 	# 	'cuenta': str(c.cuenta),
		# 	# 	'concepto': str(c.concepto()),
		# 	# 	'periodo': str(c.periodo()),
		# 	# 	'monto': "{:.2f}".format(c.monto),
		# 	# 	'detalle': c.detalle
		# 	# } for c in creditos]
		# if cobros:
		# 	objects['cobros'] = [{
		# 		'cuenta': str(c.cuenta),
		# 		'concepto': str(c.concepto()),
		# 		'periodo': str(c.periodo()),
		# 		'monto': "{:.2f}".format(c.monto),
		# 	} for c in cobros]
		# if a_cuenta

		# html_string = render_to_string(html_location, context)

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
