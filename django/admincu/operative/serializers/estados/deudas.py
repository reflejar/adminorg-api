from .base import *


class EstadoDeudasModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Deuda
	"""

	interes_generado = serializers.SerializerMethodField()
	pago_total = serializers.SerializerMethodField()
	saldo = serializers.SerializerMethodField()

	class Meta:
		model = Operacion

		fields = (
			'id',
			'interes_generado',
			'pago_total',
			'saldo'
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print(self.context['cuenta'])
		if self.context['cuenta']:
			if self.context['cuenta'].naturaleza.nombre == "cliente":
				self.fields['ingreso'] = serializers.CharField(read_only=True, max_length=150)


	def get_interes_generado(self, obj):
		if self.context['cuenta']:
			if self.context['cuenta'].naturaleza.nombre == "cliente":
				return obj.interes_generado(fecha=self.context['fecha'])
		
		return 0.00
			

	def get_pago_total(self, obj):

		return obj.pago_total(fecha=self.context['fecha'])

	def get_saldo(self, obj):

		return obj.saldo(fecha=self.context['fecha'], condonacion=self.context['condonacion'])	