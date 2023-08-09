import datetime

def obtener_fechas_lunes_a_domingo():
    hoy = datetime.datetime.now()
    dia_de_la_semana = hoy.weekday()  # 0 para lunes, 6 para domingo
    
    fecha_lunes = hoy - datetime.timedelta(days=dia_de_la_semana)
    fecha_domingo = fecha_lunes + datetime.timedelta(days=6)

    lunes = fecha_lunes.strftime("%Y-%m-%d 00:00:00")
    domingo= fecha_domingo.strftime("%Y-%m-%d 23:59:59")
    fechas_semana = {"lunes":lunes, "domingo":domingo}
    
    return fechas_semana

