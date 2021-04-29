from .base import *


class EstadoSaldosModelSerializer(EstadoBaseModelSerializer):
	"""
		Estado de Saldos a Favor
	"""

	saldo = serializers.SerializerMethodField()

	class Meta:
		model = Operacion

		fields = (
			'id',
			'saldo'
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		
	def get_saldo(self, obj):

		return obj.saldo(fecha=self.context['end_date'], condonacion=self.context['condonacion'])	