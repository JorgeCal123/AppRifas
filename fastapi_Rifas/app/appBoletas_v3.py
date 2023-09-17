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
def generar_numero(primerDigito):
    primer_numero = 0

    if primerDigito == 0:
        primer_numero = str(random.choice([3, 4]))
    if primerDigito == 1:
        primer_numero = str(random.choice([9, 8]))
    if primerDigito == 2:
        primer_numero = str(random.choice([2]))
    if primerDigito == 3:
        primer_numero = str(random.choice([7]))
    if primerDigito == 4:
        primer_numero = str(random.choice([1]))
    if primerDigito == 5:
        primer_numero = str(random.choice([6]))
    if primerDigito == 6:
        primer_numero = str(random.choice([0]))
    if primerDigito == 7:
        primer_numero = str(random.choice([5]))
    otros_tres_digitos = str(random.randint(0, 999)).zfill(3)
    
    numero = primer_numero + otros_tres_digitos

    return numero

def seleccionar_formato(cantidad_oportunidades, primerDigito):
    numero = 0
    if cantidad_oportunidades == 2:
        pass
    if cantidad_oportunidades == 3:
        pass
    if cantidad_oportunidades == 8:
        numero= generar_numero(primerDigito)
    if cantidad_oportunidades == 10:
        pass
    return numero

talonario = []

def generar_boletas(cantidad_boletas, cantidad_oportunidades):
    
    numeros_generados = set()
    id_inicial = 1
    id_final = id_inicial + cantidad_boletas - 1

    for id_boleta in range(id_inicial, id_final + 1):
        boleta = {
            "consecutiva_id": id_boleta,
            "qr_code": "xxx-xxx-xxx-xxx",
            "numeros": []
        }
        
        # Generar 8 números de 4 dígitos para cada boleta segun formato
        numeros_boleta = set()
        numeros = list()
        while len(numeros_boleta) < cantidad_oportunidades:
            numero = seleccionar_formato(cantidad_oportunidades, len(numeros_boleta))
            if numero not in numeros_generados:
                numeros_boleta.add(numero)
                numeros_generados.add(numero)
                numeros.append(numero)
        # Agregar los números a la boleta
        boleta["boletas"] = numeros
        
        talonario.append(boleta)




cantidad_boletas = 10
cantidad_oportunidades = 4

generar_boletas(cantidad_boletas, cantidad_oportunidades)
# Imprimir el talonario
for boleta in talonario:
    print(f"ID: {boleta['id']}, Cantidad de Boletas: {boleta['cantidad_boletas']}, Boletas: {', '.join(boleta['boletas'])}")
