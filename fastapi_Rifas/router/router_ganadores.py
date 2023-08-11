from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from schema.schema_premios import *
from config.conexion import get_db
from sqlalchemy.orm import Session

from modelo.modelos import Ganador
routerGanadoras = APIRouter()

"""
@routerGanadoras.get("/ganadores", response_model=List[SchemaBasicGanadores])
def mostarGanadores(db:Session = Depends(get_db)):
    ganadores = db.query(Ganador).all()
    lista_ganadores=[]
    for ganador in ganadores:
        premio = ganador.premio
        schema_ganador = SchemaGanador(fecha=premio.fecha_Juego, premio=premio.premio, boleta_ganadora=ganador.numeroGanador)
        lista_ganadores.append(schema_ganador)
    basic_ganadores= SchemaBasicGanadores(ganadores=lista_ganadores)
    return basic_ganadores

"""
