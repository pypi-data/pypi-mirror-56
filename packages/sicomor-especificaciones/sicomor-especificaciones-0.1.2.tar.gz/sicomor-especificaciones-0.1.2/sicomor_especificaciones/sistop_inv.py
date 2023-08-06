# identificador xxyyzzzz
# xx-> tipo1: 10: HW
#             11: SW
# yy-> tipo2: SW: 01 SISTOP

SISTOP_INV = [
	{	"tipo1": "SW",
		"tipo2": "SISTOP",
		"identificador": 10010001,
		"descripcion": "Nombre completo Sistema Operativo",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "SistemaOperativo",
					  "function": "get_items"}, }
]