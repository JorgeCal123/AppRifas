import math
import pandas as pd

# Definir las variables n y k
n = 10  # Número total de elementos disponibles (dígitos del 0 al 9)
k = 3   # Número de elementos a elegir (3 dígitos)

# Calcular la combinación C(n, k)
combinacion = math.comb(n, k)

# Imprimir el resultado
print(f"El número de combinaciones de {k} dígitos sin repetir de un conjunto de {n} dígitos es {combinacion}")

# Generar todas las combinaciones de números de 0 al 9 elegidos en grupos de 3
combinaciones = []

for i in range(10):
    for j in range(10):
        for k in range(10):
            if i != j and i != k and j != k:
                combinacion = [i, j, k]
                combinaciones.append(combinacion)

# Crear un DataFrame de pandas con las combinaciones
df = pd.DataFrame(combinaciones, columns=['Columna1', 'Columna2', 'Columna3'])

# Guardar el DataFrame en un archivo Excel
df.to_excel('combinaciones.xlsx', index=False)

print("Combinaciones guardadas en el archivo 'combinaciones.xlsx'")
