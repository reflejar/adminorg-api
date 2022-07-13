MODULE = {
	'name': "Cuentas a cobrar",
	'path': 'front:clientes:index'
}

MODULE_HANDLER = "cliente"

TEMPLATE_FOLDER = "modules/clientes/"

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
        "label": "+ Cargas/Cobros"
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

