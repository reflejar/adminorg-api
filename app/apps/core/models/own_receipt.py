from django.db import models
from django_afip.models import *


class OwnReceipt(models.Model):
	"""
		Modelo para receipt en "Documento".

		Se toma como base el modelo de django afip. 
		El de afip queda unicamente para replicar los objetos que hay en este cuando el Documento es 
		de un cliente y se necesite validar en afip
	"""

	point_of_sales = models.PositiveSmallIntegerField(
		blank=True,null=True,
		verbose_name="point of sales",
	)
	receipt_type = models.ForeignKey(
		ReceiptType,
		related_name="own_receipts",
		verbose_name="receipt type",
		on_delete=models.PROTECT,
	)
	concept = models.ForeignKey(
		ConceptType,
		blank=True,null=True,
		related_name="own_receipts",
		verbose_name="concept",
		on_delete=models.PROTECT,
	)
	document_type = models.ForeignKey(
		DocumentType,
		blank=True,null=True,
		related_name="own_receipts",
		verbose_name="document type",
		on_delete=models.PROTECT,
	)
	document_number = models.BigIntegerField(
		"document number",
		blank=True, null=True
	)
	receipt_number = models.PositiveIntegerField(
		"receipt number",
		null=True, blank=True,
	)
	issued_date = models.DateField(
		verbose_name="issued date",
	)
	total_amount = models.DecimalField(
		"total amount",
		max_digits=15,
		decimal_places=2,
	)
	net_untaxed = models.DecimalField(
		"total untaxable amount",
		max_digits=15,
		decimal_places=2,
	)
	net_taxed = models.DecimalField(
		"total taxable amount",
		max_digits=15,
		decimal_places=2,
	)
	exempt_amount = models.DecimalField(
		"exempt amount",
		max_digits=15,
		decimal_places=2,
	)
	service_start = models.DateField(
		"service start date",
		null=True, blank=True,
	)
	service_end = models.DateField(
		"service end date",
		null=True, blank=True,
	)
	expiration_date = models.DateField(
		"receipt expiration date",
		null=True, blank=True,
	)
	currency = models.ForeignKey(
		CurrencyType,
		blank=True,null=True,
		verbose_name="currency",
		related_name="own_receipts",
		on_delete=models.PROTECT,
		default=first_currency,
	)
	currency_quote = models.DecimalField(
		"currency quote",
		blank=True,null=True,
		max_digits=10,
		decimal_places=6,
		default=1,
	)

	@property
	def formatted_number(self):
		"""This receipt's number in the usual format: ``0001-00003087``."""
		if self.receipt_number:
			name = ""
			if self.point_of_sales:
				name += "{:04d}-".format(int(self.point_of_sales))
			name += "{:08d}".format(self.receipt_number)
			return name
		return None


	def __repr__(self):
		return "<Receipt {}: {} {} for {}>".format(
			self.pk,
			self.receipt_type,
			self.receipt_number,
		)

	def __str__(self):
		if self.receipt_number:
			return "{} {}".format(self.receipt_type, self.formatted_number)
		else:
			return "%s S/N" % self.receipt_type
