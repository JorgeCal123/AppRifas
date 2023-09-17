import random

# Función para generar números aleatorios que cumplan con la estructura deseada
def generar_numero():
    primer_numero = str(random.choice([3, 4]))
    segundo_numero = str(random.choice([9, 8]))
    tercer_numero = str(random.choice([2]))
    cuarto_numero = str(random.choice([7]))
    quinto_numero = str(random.choice([1]))
    sexto_numero = str(random.choice([6]))
    septimo_numero = str(random.choice([0]))
    octavo_numero = str(random.choice([5]))
    
    # Combinar los números para formar un número de 4 dígitos
    numero_completo = "".join([primer_numero, segundo_numero, tercer_numero, cuarto_numero, quinto_numero, sexto_numero, septimo_numero, octavo_numero])
    
    return numero_completo

# Definir el número de boletas a generar y el rango de IDs
cantidad_boletas = 2
id_inicial = 1
id_final = id_inicial + cantidad_boletas - 1

# Crear el talonario con la información de las boletas
talonario = []

# Conjunto para almacenar números generados en todas las boletas
numeros_generados = set()

for id_boleta in range(id_inicial, id_final + 1):
    boleta = {
        "id": id_boleta,
        "cantidad_boletas": cantidad_boletas,
        "boletas": []
    }
    
    # Generar 8 números aleatorios para cada boleta
    numeros_boleta = set()
    while len(numeros_boleta) < 8:
        numero = generar_numero()
        if numero not in numeros_generados:
            numeros_boleta.add(numero)
            numeros_generados.add(numero)
    
    # Agregar los números a la boleta
    boleta["boletas"] = list(numeros_boleta)
    
    talonario.append(boleta)

# Imprimir el talonario
for boleta in talonario:
    print(f"ID: {boleta['id']}, Cantidad de Boletas: {boleta['cantidad_boletas']}, Boletas: {', '.join(boleta['boletas'])}")
