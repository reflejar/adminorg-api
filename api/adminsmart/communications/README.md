# Modulo de comunicaciones

### Qué soy?

Módulo que almacena y ejecuta todos los envíos (comunicaciones) que salen de la aplicación
Los demás modulos de adminsmart se comunican conmigo para realizar envíos 

### A donde envío la información?

Cuando salga de aqui una comunicación puede:
- Enviarse por mail al socio, usuario, etc.
- Hacia las plataformas que se encargan de hacerlo (a la fecha: Simple Solutions, Expensas Pagas)

### Cómo hago?

Tengo una tarea de celery vinculada para ejecutarse (actualmente cada 30 segundos) en la que "atiendo la cola" (ola, usté que quiere?)
Y ejecuto su solicitud

### Por dónde la ejecuto?

Lo meto por la pasarela de envíos (gateway.py) y ejecuto el metodo .send() de cada _Dispatcher..._ (...más abajo)

### Cómo me estructuro? 

#### Modelos

| Nombre | Qué hace |
| ------ | ------ |
| BaseComunnication | Modelo base para las comunicaciones |
| Queue | Cola de envios |
| Execution | Envios ejecutados |
| Attachment | Adjuntos de los envios - archivos y cosas |


#### Providers

Son los proveedores/canales de comuncación hacia el socio/cliente
Cada Provider tiene un Dispatcher que se encarga de su propia logica de envío. (Metodo importante: .send()

| Nombre | Cómo hace |
| ------ | ------ |
| mail | Envía directo por mail al socio si la comunidad está autorizada para realizar envios por mails |
| simple_solutions | La lógica está linkeada con la propia del modulo platforms/simple_solutions (But it's not done yet) |
| expensas_pagas | La lógica está linkeada con la propia del modulo platforms/expensas_pagas (But it's not done yet) |
