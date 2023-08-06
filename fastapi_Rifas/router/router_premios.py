from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from schema.schema_premios import *

from sqlalchemy.orm import Session

from config.conexion import get_db
from modelo.modelos import Talonario


routerPremios = APIRouter()


@routerPremios.get("/juegos",response_model=List[SchemaInfoJuegos])
def mostrar_info_juegos(db:Session=Depends(get_db)):
  
    """
  select premio, fecha_juego, numero_ganador
  from Premios
  join Ganador
  on premios.id = ganador.premio_id
  where fecha_juego between fecha inicial y fecha final 
  
  query = db.query(Premios.premio, Premios.fecha_juego, Premios.numero_ganador).\
    join(Ganador, Premios.id == Ganador.premio_id).\
    filter(and_(Premios.fecha_juego >= fecha_inicial, Premios.fecha_juego <= fecha_final))

# Obtener los resultados
resultados = query.all()
"""
    talonarios = db.query(Talonario).all()
    lista_premios=[] 
    for talonario in talonarios:
        for premio in talonario.premios:
            lista_premios.append(premio)

    schem_info_juegos = []

    for indice_actual in range(len(lista_premios)):
        list_nombre_premios= []
        num_ganadores= []
        fecha1 = lista_premios[indice_actual].fecha_Juego.strftime("%Y-%m-%d")
        list_nombre_premios.append(lista_premios[indice_actual].premio)
        num_ganadores.append(lista_premios[indice_actual].ganador.numeroGanador)
        info_juegos=SchemaInfoJuegos(dia=lista_premios[indice_actual].fecha_Juego.strftime("%A"), fecha= lista_premios[indice_actual].fecha_Juego, premio=list_nombre_premios, ganador = num_ganadores)
        
        for indice_siguiente in range(indice_actual + 1, len(lista_premios) ):
            fecha2 = lista_premios[indice_siguiente].fecha_Juego.strftime("%Y-%m-%d")
            if fecha1 == fecha2:
                list_nombre_premios.append(lista_premios[indice_actual].premio)
                num_ganadores.append(lista_premios[indice_actual].ganador.numeroGanador)
                #lista_premios.pop(indice_siguiente)
        info_juegos.premio = list_nombre_premios
        info_juegos.ganador= num_ganadores
        schem_info_juegos.append(info_juegos)
    return schem_info_juegos
