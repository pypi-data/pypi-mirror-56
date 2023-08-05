# identificador xxyyzzzz
# xx-> tipo1: 10: HW
#             11: SW
# yy-> tipo2: HW: 01 PROC
# 			      10 MEM
# 			      11 DISK

HARDWARE_INV = [
	####################
	#      MEMORIA     #
	####################
	{	"tipo1": "HW",
		"tipo2": "MEM",
		"identificador": 10100001,
		"descripcion": "Memoria Fisica Total Disponible",
		"unidad": "bytes",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "Memoria",
					  "function": "get_total_virt"}, },
	{	"tipo1": "HW",
		"tipo2": "MEM",
		"identificador": 10100002,
		"descripcion": "Tipo de Memorias Instaladas",
		"unidad": "str",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "",
					  "function": ""}, },
	{	"tipo1": "HW",
		"tipo2": "MEM",
		"identificador": 10100003,
		"descripcion": "Fabricante de Memorias Instaladas",
		"unidad": "str",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "",
					  "function": ""}, },
	{	"tipo1": "HW",
		"tipo2": "MEM",
		"identificador": 10100004,
		"descripcion": "Tamaño de Memorias",
		"unidad": "gb",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "",
					  "function": ""}, },

	####################
	#       DISCO      #
	####################
	{	"tipo1": "HW",
		"tipo2": "DISK",
		"identificador": 10110001,
		"descripcion": "Tamaño total de discos",
		"unidad": "gb",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "",
					  "function": ""}, },
	{	"tipo1": "HW",
		"tipo2": "DISK",
		"identificador": 10110002,
		"descripcion": "Fabricante de discos instalados",
		"unidad": "str",
		"estado": True,
		# ----------------------------------------------------
		"manejador": {"id": 1,
					  "clase": "",
					  "function": ""}, }
	]
