MODULE = {
	'name': "Stock",
	'path': 'front:stock:index'
}

MODULE_HANDLER = "bien_de_cambio"

TEMPLATE_FOLDER = "modules/tesoreria/"

MODULE_BUTTONS = [
    {
        "path": "front:stock:create",
        "label": "Nuevo producto"
    },
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:stock:cbte-create",
        "label": "+ Transferencia internas"
    },    
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:stock:registros",
        "label": "Registro de transferencias"
    },           

]

