MODULE = {
	'name': "Contabilidad",
	'path': 'front:contabilidad:index'
}

MODULE_HANDLER = "titulo"

TEMPLATE_FOLDER = "modules/contabilidad/"

MODULE_BUTTONS = [
    {
        "path": "front:contabilidad:create",
        "label": "Nuevo titulo"
    },
    {
        "path": "",
        "label": "---"
    },
    {
        "path": "front:contabilidad:cbte-create",
        "label": "+ Asiento"
    },
    {
        "path": "",
        "label": "---"
    },    
    {
        "path": "front:contabilidad:registros",
        "label": "Registro de asientos"
    },        
    {
        "path": "front:contabilidad:mayores",
        "label": "Mayores"
    },       

]

