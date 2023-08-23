import datetime

"""
    Obtine la fecha del lunes y domingo a partir de la fecha actual

    Esta función toma la fecha actual y calcula cuando cae lunes y cuando cae domingo

    Returns:
        dict: Un diccionario donde las llaves son lunes y domingo y contiene sus respectivas fechas

"""
def obtener_fechas_lunes_a_domingo():
    hoy = datetime.datetime.now()
    dia_de_la_semana = hoy.weekday()  # 0 para lunes, 6 para domingo
    
    fecha_lunes = hoy - datetime.timedelta(days=dia_de_la_semana)
    fecha_domingo = fecha_lunes + datetime.timedelta(days=6)

    lunes = fecha_lunes.strftime("%Y-%m-%d 00:00:00")
    domingo= fecha_domingo.strftime("%Y-%m-%d 23:59:59")
    fechas_semana = {"lunes":lunes, "domingo":domingo}
    
    return fechas_semana

"""
    Obtine la fecha de hace 15 días a partir de la fecha actual

    Esta función toma la fecha actual y calcula la fecha de hace 15 días atras

    Returns:
        dict: Un diccionario donde las llaves son actual y dos_semanas_atras que
              contiene sus respectivas fechas

"""
def obtener_fechas_jugadas():
    hoy = datetime.datetime.now()
    
    fecha_actual = hoy
    dos_semanas_atras = fecha_actual - datetime.timedelta(days=15)

    actual = fecha_actual.strftime("%Y-%m-%d 00:00:00")
    semanas_atras= dos_semanas_atras.strftime("%Y-%m-%d 23:59:59")
    fechas_semana = {"actual":actual, "dos_semanas_atras":semanas_atras}
    
    return fechas_semana
