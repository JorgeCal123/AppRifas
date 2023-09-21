from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from schema.schema_premios import *

from sqlalchemy.orm import Session

from config.conexion import get_db
from modelo.modelos import *
from app.fechas_semana import *
import datetime
from datetime import datetime

routerPremios = APIRouter()


@routerPremios.get("/juegosemanal",response_model=List[SchemaInfoJuegos], tags=["Premios"])
def mostrar_info_juegos(db:Session=Depends(get_db)):
 
    info_premio = db.query(Premio.premio, Premio.fecha_juego, Ganador.numero_ganador) \
    .outerjoin(Ganador, Premio.id == Ganador.id_premio) \
    .filter(Premio.fecha_juego.between(obtener_fechas_lunes_a_domingo()["lunes"],  obtener_fechas_lunes_a_domingo()["domingo"])) \
    .all()

    dict_premio = formato_info_juego(info_premio)

    info_juegos = []
    for fecha, juego in dict_premio.items():
       fecha = datetime.strptime(fecha, '%d-%m-%Y')

       schema_info_juegos = SchemaInfoJuegos(dia = fecha.strftime("%A"), premios = juego, fecha= fecha.strftime("%d-%m-%Y"))
       info_juegos.append(schema_info_juegos)
    
    return info_juegos


"""
    Formatea la información de premios y ganadores en un diccionario agrupado por fechas.

    Esta función toma una lista de información de premios y ganadores y la organiza
    en un diccionario donde las fechas de los premios son las llaves, y los valores
    asociados son listas de información de ganadores y premios para esa fecha.

    Args:
        info_premio (list): Una lista de objetos que contienen información de premios y ganadores.
                           Cada objeto debe tener atributos 'fecha_juego', 'premio' y 'numero_ganador'.

    Returns:
        dict: Un diccionario donde las llaves son fechas formateadas en formato 'dd-mm-yyyy',
              y los valores son listas de objetos SchemaInfoGanador, que contienen información de premios
              y ganadores, y opcionalmente el numero ganador.

"""
def formato_info_juego(info_premio):
    dict_premio = {}
    premio_lista = []
    for premio in info_premio:
      fecha_premio = premio.fecha_juego.strftime("%d-%m-%Y")
      if fecha_premio not in dict_premio:
        premio_lista = []
        juego = SchemaInfoGanador(premio = premio.premio, ganador= premio.numero_ganador)
        premio_lista.append(juego)
        dict_premio[fecha_premio] = premio_lista
      else:
        lista_nueva_premios= dict_premio.get(fecha_premio)
        juego = SchemaInfoGanador(dia = premio.fecha_juego.strftime("%A"),premio = premio.premio, ganador= premio.numero_ganador)
        lista_nueva_premios.append(juego)
        dict_premio[fecha_premio] = lista_nueva_premios
    return dict_premio


@routerPremios.get("/juegospasados",response_model=List[SchemaJuegosPasados], tags=["Premios"])
def mostrar_juegos_pasados(db:Session=Depends(get_db)):
 
    info_premio = db.query(Premio.premio, Premio.fecha_juego, Ganador.numero_ganador) \
    .join(Ganador, Premio.id == Ganador.id_premio) \
    .filter(Premio.fecha_juego.between(obtener_fechas_jugadas()["dos_semanas_atras"], obtener_fechas_jugadas()["actual"])) \
    .all()
    juegos_pasados= []
    for juegos in info_premio:
      juego = SchemaJuegosPasados(fecha=juegos.fecha_juego.strftime("%d-%m-%Y"), premio= juegos.premio, boleta_ganadora= juegos.numero_ganador)
      juegos_pasados.append(juego)
    return juegos_pasados
    