from rest_framework import serializers

from adminsmart.apps.informes.analisis import OperacionAnalisis

GROUPS = [
	('periodo', 'Periodo'),
	('concepto', 'Concepto'),
	('tipo_documento', 'Tipo Documento')
]

TOTALIZERS = [
	('debe', 'Debe y Haber'),
	('valor', 'Valor'),
	('cantidad', 'Cantidad')
]

class InformeSerializer(serializers.Serializer):
	'''Informe model serializer'''

	start_date = serializers.DateField(
		allow_null=True,
		label="Desde"
	)

	end_date = serializers.DateField(
		allow_null=True,
		label="Hasta"
	)
	
	analizar = serializers.ChoiceField(
			choices=[
				('cliente', 'Clientes'),
				('proveedor', 'Proveedores'),
			],
			label="Analizar"
		)
	agrupar_por = serializers.ChoiceField(
			choices=GROUPS,
			label="Agrupar por"
		)
	encolumnar = serializers.ChoiceField(
			choices=GROUPS,
			label="Encolumnar"
		)
	totalizar = serializers.ChoiceField(
			choices=TOTALIZERS,
			label="Totalizar"
		)

	def create(self, validated_data):
		pd = OperacionAnalisis(validated_data)
		print(pd)
		return validated_data