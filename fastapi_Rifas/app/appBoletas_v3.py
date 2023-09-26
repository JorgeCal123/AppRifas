import random


"""
{
    "Boleta": {
        "id": 198675,
        "consecutiva_id": 1,
        "qr_code": "EjemploQR123",
        "estado_venta": false,
        "estado_pagado": false,
        "fecha_venta": None,
        "id_talonario": 123456,
        "numeros": [
                    12345
                    67890
                    ],
        "ganador": {
                    "id": 101,
                    "descripcion": "Ganador del premio principal"
                    },
        "id_cliente": 201,
        "id_vendedor": 301
    }
"""

class MiErrorPersonalizado(Exception):
    def __init__(self):
        self.mensaje = "Error: La cantidad de oportunidades registradas hasta el momento es de 10, 8, 3 y 2"

def generar_numero_dos_oportunidades(primerDigito):
    primer_numero = 0

    if primerDigito == 0:
        primer_numero = str(random.choice([5,6,7,8,9]))

    elif primerDigito == 1:
        primer_numero = str(random.choice([0,1,2,3,4]))

    otros_tres_digitos = str(random.randint(0, 999)).zfill(3)
    
    numero = primer_numero + otros_tres_digitos

    return numero
def generar_numero_tres_oportunidades(primerDigito):
    primer_numero = 0

    if primerDigito == 0:
        primer_numero = str(random.choice([7,8,9]))
    elif primerDigito == 1:
        primer_numero = str(random.choice([4,5,6]))
    elif primerDigito == 2:
        primer_numero = str(random.choice([0,1,2,3]))

    otros_tres_digitos = str(random.randint(0, 999)).zfill(3)
    
    numero = primer_numero + otros_tres_digitos

    return numero
def generar_numero_ocho_oportunidades(primerDigito):
    primer_numero = 0

    if primerDigito == 0:
        primer_numero = str(random.choice([3, 4]))
    elif primerDigito == 1:
        primer_numero = str(random.choice([9, 8]))
    elif primerDigito == 2:
        primer_numero = str(2)
    elif primerDigito == 3:
        primer_numero = str(7)
    elif primerDigito == 4:
        primer_numero = str(1)
    elif primerDigito == 5:
        primer_numero = str(6)
    elif primerDigito == 6:
        primer_numero = str(0)
    elif primerDigito == 7:
        primer_numero = str(5)
    otros_tres_digitos = str(random.randint(0, 999)).zfill(3)
    
    numero = primer_numero + otros_tres_digitos

    return numero

def generar_numero_dies_oportunidades(primerDigito):
    primer_numero = 0

    if primerDigito == 0:
        primer_numero = str(3)
    elif primerDigito == 1:
        primer_numero = str(4)
    elif primerDigito == 2:
        primer_numero = str(9)
    elif primerDigito == 3:
        primer_numero = str(8)
    elif primerDigito == 4:
        primer_numero = str(2)
    elif primerDigito == 5:
        primer_numero = str(7)
    elif primerDigito == 6:
        primer_numero = str(1)
    elif primerDigito == 7:
        primer_numero = str(6)
    elif primerDigito == 6:
        primer_numero = str(0)
    elif primerDigito == 7:
        primer_numero = str(5)
    otros_tres_digitos = str(random.randint(0, 999)).zfill(3)
    
    numero = primer_numero + otros_tres_digitos

    return numero

def seleccionar_formato(cantidad_oportunidades, primerDigito):
    numero = 0
    if cantidad_oportunidades == 2:
        numero = generar_numero_dos_oportunidades(primerDigito)
    elif cantidad_oportunidades == 3:
        numero = generar_numero_tres_oportunidades(primerDigito)
    elif cantidad_oportunidades == 8:
        numero = generar_numero_ocho_oportunidades(primerDigito)
    elif cantidad_oportunidades == 10:
        numero = generar_numero_dies_oportunidades(primerDigito)
    else:
        raise MiErrorPersonalizado()

    return numero


def generar_boletas(cantidad_boletas, cantidad_oportunidades):
    talonario = []
    numeros_generados = set()
    id_inicial = 1
    id_final = id_inicial + cantidad_boletas - 1

    for id_boleta in range(id_inicial, id_final + 1):
        boleta = {
            "consecutiva_id": id_boleta,
            "qr_code": "xxx-xxx-xxx-xxx",
        }
        # Generar 8 números de 4 dígitos para cada boleta segun formato
        numeros_boleta = set()
        numeros = list()

        while len(numeros_boleta) < cantidad_oportunidades:
            numero = 0
            try:
                numero = seleccionar_formato(cantidad_oportunidades, len(numeros_boleta))
            except MiErrorPersonalizado as error:
               print(error.mensaje)
               return
            if numero not in numeros_generados:
                numeros_boleta.add(numero)
                numeros_generados.add(numero)
                numeros.append(numero)
        # Agregar los números a la boleta
        boleta["numeros"] = numeros
        
        talonario.append(boleta)
    return talonario

"""

cantidad_boletas = 10
cantidad_oportunidades = 7

generar_boletas(cantidad_boletas, cantidad_oportunidades)
# Imprimir el talonario
for boleta in talonario:
    print(f"consecutiva_id: {boleta['consecutiva_id']}, qr_code: {boleta['qr_code']}, Boletas: {', '.join(boleta['boletas'])}")
"""