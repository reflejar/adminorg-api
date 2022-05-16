MODULE = {
	'name': "Cuentas a cobrar",
	'path': 'front:clientes:index'
}

TEMPLATE_FOLDER = "clientes/"

MODULE_BUTTONS = [
    {
        "path": "front:clientes:create",
        "label": "Nuevo cliente"
    },
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:clientes:pre-operaciones",
        "label": "Pre conceptos"
    },
    {
        "path": "front:clientes:cbte-masivo",
        "label": "+ Comprobantes masivos"
    },    
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:clientes:registros",
        "label": "Registro de comprobantes"
    },           

]

