import random
import pprint

cero = {0:[]}
uno = {1:[]}
dos = {2:[]}
tres = {3:[]}
cuatro = {4:[]}
cinco = {5:[]}
seis = {6:[]}
siete = {7:[]}
ocho = {8:[]}
nueve = {9:[]}

talonario = {}
def llenarListas():
    global talonario, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, cero

    for x in range(0, 999):
        if x >= 100:
            cero[0].append(x)
        uno[1].append(x)
        dos[2].append(x)
        tres[3].append(x)
        cuatro[4].append(x)
        cinco[5].append(x)
        seis[6].append(x)
        siete[7].append(x)
        ocho[8].append(x)
        nueve[9].append(x)

"""
{
      "id": 0,
      "id_talonario": 0,
      "id_cliente": 0,
      "id_vendedor": 0,
      "qr_code": "string",
      "detalle": "string",
      "pagado": true,
      "fecha_venta": "2023-07-30T18:50:40.629Z"
    }
"""
def crearBoleta(cantidadboletas):
    llenarListas()
    global talonario, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, cero
    for x in range(cantidadboletas):
        numeros = []
        boleta = {}
        numeros.clear()
        boleta["qr_code"] = "xxxx - xxxx -xxxx"
        numeros.append(sacarnumeroList(random.randint(0, len(cuatro[4]) -1 ), cuatro))
        numeros.append(sacarnumeroList(random.randint(0, len(dos[2]) -1 ), dos))
        numeros.append(sacarnumeroList(random.randint(0, len(uno[1]) -1 ), uno))
        numeros.append(sacarnumeroList(random.randint(0, len(tres[3]) -1 ), tres))
        numeros.append(sacarnumeroList(random.randint(0, len(ocho[8]) -1 ), ocho))
        numeros.append(sacarnumeroList(random.randint(0, len(siete[7]) -1 ), siete))
        numeros.append(sacarnumeroList(random.randint(0, len(seis[6]) -1 ), seis))
        numeros.append(sacarnumeroList(random.randint(0, len(cinco[5]) -1 ), cinco)) 
        boleta["numeros"] = numeros
        talonario[str(x)] = boleta

def sacarnumeroList(aleatorio, dict_list):
    global talonario, uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, cero

    llave = 0
    for key in dict_list: llave = key
    numero = dict_list[llave][aleatorio]
    dict_list[llave].pop(aleatorio)
    digitos = 3 - len(str(numero))
    serie = str(llave)
    for concatenar in range(digitos):
        serie = serie + "0"
    serie = serie + str(numero)
    return serie

def clearlistas():
    cero[0].clear()
    uno[1].clear()
    dos[2].clear()
    tres[3].clear()
    cuatro[4].clear()
    cinco[5].clear()
    seis[6].clear()
    siete[7].clear()
    ocho[8].clear()
    nueve[9].clear()

def startCreateBoletas(cantidad:int):
    if(cantidad > 1000):
        print("La cantidad debe ser menor a 1000")
    crearBoleta(cantidad)
    clearlistas()
    return talonario

