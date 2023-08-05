from .hardware_inv import HARDWARE_INV
from .sistop_inv   import SISTOP_INV
from .software_inv import SOFTWARE_INV

INVENTARIO = HARDWARE_INV + SISTOP_INV + SOFTWARE_INV


def get_recursos():
	"""
		Retorna lista de inventarios validos.
	"""
	recursos = []
	for x in INVENTARIO:
		if x["estado"]:
			recursos.append(x)
	return recursos


def get_recurso(identificador):
	for x in INVENTARIO:
		if x["identificador"] == int(identificador):
			return x
	return {}
