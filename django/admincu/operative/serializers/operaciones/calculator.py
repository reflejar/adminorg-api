from .base import *

class CalculatorModelSerializer(OperacionModelSerializer):
	"""
		Base de Operaciones para Estados e Informes
	"""
	numero_asiento = serializers.SerializerMethodField()
	documento_tipo = serializers.SerializerMethodField()
	documento_numero = serializers.SerializerMethodField()
	titulo_numero = serializers.SerializerMethodField()
	titulo_nombre = serializers.SerializerMethodField()
	concepto = serializers.SerializerMethodField()
	capital = serializers.SerializerMethodField()
	interes = serializers.SerializerMethodField()
	total = serializers.SerializerMethodField()	
	pago_capital = serializers.SerializerMethodField()	

	class Meta:
		model = Operacion

		fields = (
			'monto',
			'capital',
			'interes',
			'total',
			'valor',
			'debe',
			'haber',		
			'saldo',
			'pago_capital',
			'cuenta',
			'detalle',
			'concepto',
			'documento_tipo',
			'documento_numero',
			'naturaleza',
			'fecha',
			'periodo',
			'cantidad',
			'fecha_vencimiento',
			'fecha_gracia',
			'descripcion',
			'numero_asiento',
			'titulo_nombre',
			'titulo_numero'
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['cuenta'] = serializers.CharField(max_length=200)
		self.numero_asiento = 1
		self.capital = 0.00
		self.interes = 0.00
		self.saldo = 0.00
		self.total = 0.00
		self.pago_capital = 0.00


	# show functions
	def get_numero_asiento(self, obj):
		return self.numero_asiento

	def get_documento_tipo(self, obj):
		return obj.documento.receipt.receipt_type.description

	def get_documento_numero(self, obj):
		return obj.documento.receipt.formatted_number

	def get_titulo_numero(self, obj):
		return obj.cuenta.titulo.numero

	def get_titulo_nombre(self, obj):
		return obj.cuenta.titulo.nombre		

	def get_concepto(self, obj):
		if obj.concepto():
			return str(obj.concepto())
		return None		

	# calc functions
	def get_capital(self, obj):
		return self.capital

	def get_interes(self, obj):
		return self.interes

	def get_total(self, obj):
		return self.total

	def get_saldo(self, obj):
		return self.saldo

	def get_pago_capital(self, obj):
		return self.pago_capital		