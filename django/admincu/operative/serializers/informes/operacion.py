from rest_framework import serializers

from admincu.operative.models import Operacion

class InformesModelSerializer(serializers.ModelSerializer):
	
	'''Operacion para la parte informes'''

	capital = serializers.SerializerMethodField()
	interes = serializers.SerializerMethodField()
	total = serializers.SerializerMethodField()
	concepto = serializers.SerializerMethodField()
	numero_asiento = serializers.SerializerMethodField()
	documento_tipo = serializers.SerializerMethodField()
	documento_numero = serializers.SerializerMethodField()
	titulo_numero = serializers.SerializerMethodField()
	titulo_nombre = serializers.SerializerMethodField()
	
	class Meta:
		model = Operacion

		fields = (
			'id',
			'cuenta',
			'documento_tipo',
			'documento_numero',
			'detalle',
			'naturaleza',
			'fecha',
			'concepto',
			'periodo',
			'cantidad',
			'fecha_vencimiento',
			'fecha_gracia',
			'detalle',
			'descripcion',
			'monto',
			'capital',
			'interes',
			'total',
			'valor',
			'debe',
			'haber',			
			'numero_asiento',
			'titulo_numero',
			'titulo_nombre'
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.numero_asiento = 1
		self.fields['cuenta'] = serializers.CharField(max_length=200)

	def get_capital(self, obj):
		return obj.saldo(condonacion=True)

	def get_interes(self, obj):
		return obj.interes(fecha=self.context['end_date'])

	def get_total(self, obj):
		return obj.saldo(fecha=self.context['end_date'])

	def get_concepto(self, obj):
		if obj.concepto():
			return str(obj.concepto())
		return None		

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