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
    {"tipo1": "HW",
     "tipo2": "MEM",
     "identificador": 10100001,
     "descripcion": "Memoria Fisica Total Disponible",
     "estado": True,
     # ----------------------------------------------------
     "manejador": {"id": 1,
     			   "clase": "Memoria",
     			   "function": "get_all_virt"}, },
    {"tipo1": "HW",
     "tipo2": "MEM",
     "identificador": 10100002,
     "descripcion": "Memoria Fisica Por SLOTs",
     "estado": True,
     # ----------------------------------------------------
     "manejador": {"id": 1,
     			   "clase": "Memoria",
     			   "function": "get_items"}, },
]
