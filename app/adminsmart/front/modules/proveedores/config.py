MODULE = {
	'name': "Cuentas a pagar",
	'path': 'front:proveedores:index'
}

TEMPLATE_FOLDER = "modules/proveedores/"

MODULE_BUTTONS = [
    {
        "path": "front:proveedores:create",
        "label": "Nuevo proveedor"
    },
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:proveedores:pre-operaciones",
        "label": "+ Cargas/Pagos"
    },
    {
        "path": "front:proveedores:cbte-masivo",
        "label": "+ Comprobantes masivos"
    },    
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:proveedores:registros",
        "label": "Registro de comprobantes"
    },           

]

