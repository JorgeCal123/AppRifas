from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from schema.schema_premios import *

from sqlalchemy.orm import Session

from config.conexion import get_db
from modelo.modelos import *
from app.fechas_semana import obtener_fechas_lunes_a_domingo
import datetime

routerPremios = APIRouter()


@routerPremios.get("/juegos",response_model=List
                   [SchemaInfoJuegos])
def mostrar_info_juegos(db:Session=Depends(get_db)):
 
    info_premio = db.query(Premio.premio, Premio.fecha_juego, Ganador.numero_ganador) \
    .outerjoin(Ganador, Premio.id == Ganador.id_premio) \
    .filter(Premio.fecha_juego.between(obtener_fechas_lunes_a_domingo()["lunes"],  obtener_fechas_lunes_a_domingo()["domingo"])) \
    .all()

    dict_premio = {}
    premio_lista = []
    for premio in info_premio:
      if premio.fecha_juego not in dict_premio:
        premio_lista = []
        premio_lista.append(premio.premio)
        dict_premio[premio.fecha_juego] = premio_lista
      else:
        lista_nueva_premios= dict_premio.get(premio.fecha_juego)
        lista_nueva_premios.append(premio.premio)
        dict_premio[premio.fecha_juego] = lista_nueva_premios
    print(dict_premio)
    
    
    info_juegos = []
    info_ganador = []
    for premio in info_premio:
      
      ganador = SchemaInfoGanador(premio = premio.premio,
                                  ganador = premio.numero_ganador )
      info_ganador.append(ganador)
      juego = SchemaInfoJuegos(dia = premio.fecha_juego.strftime
                               ("%A"), premios = info_ganador, fecha = premio.fecha_juego)
      info_juegos.append(juego)
      
    return info_juegos
   
