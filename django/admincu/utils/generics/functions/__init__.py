import random
import string

# Identificador aleatorio
def randomIdentifier(modelo, campo):
	query = False
	identifier = 0
	while query == False:
		aleatorio = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(30)])
		try:
			filtro = {campo: aleatorio}
			identifier = modelo.objects.get(**filtro)
		except:
			identifier = aleatorio
			query = True
	return identifier