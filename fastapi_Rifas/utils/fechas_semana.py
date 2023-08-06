import datetime

def obtener_fechas_lunes_a_domingo():
    hoy = datetime.datetime.now()
    dia_de_la_semana = hoy.weekday()  # 0 para lunes, 6 para domingo
    
    fecha_lunes = hoy - datetime.timedelta(days=dia_de_la_semana)
    fecha_domingo = fecha_lunes + datetime.timedelta(days=6)
    
    fechas_semana = [fecha_lunes + datetime.timedelta(days=i) for i in range(7)]
    
    return fechas_semana

# Obtener las fechas de lunes a domingo de la semana actual
fechas_semana_actual = obtener_fechas_lunes_a_domingo()

# Imprimir las fechas
for fecha in fechas_semana_actual:
    print(fecha.strftime('%Y-%m-%d'))

