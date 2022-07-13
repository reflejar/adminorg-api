MODULE = {
	'name': "Tesorería",
	'path': 'front:tesoreria:index'
}

MODULE_HANDLER = "caja"

TEMPLATE_FOLDER = "modules/tesoreria/"

MODULE_BUTTONS = [
    {
        "path": "front:tesoreria:create",
        "label": "Nueva caja"
    },
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:tesoreria:cbte-create",
        "label": "+ Transferencia entre cajas"
    },    
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:tesoreria:registros",
        "label": "Registro de transferencias"
    },           

]

