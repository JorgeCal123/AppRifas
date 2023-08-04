from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from schema.schema_premios import *
from config.conexion import get_db
from sqlalchemy.orm import Session

from model.models import ModelGanador
routerGanadoras = APIRouter()


@routerGanadoras.get("/ganadores", response_model=List[Schema_basic_ganadores])
def showGanadores(db:Session = Depends(get_db)):
    ganadores = db.query(ModelGanador).all()
    winners=[]
    for ganador in ganadores:
        premio = ganador.premio
        winner = Schema_ganador(fecha=premio.fecha_Juego, premio=premio.premio, boleta_ganadora=ganador.numeroGanador)
        winners.append(winner)
    schemaWinners= Schema_basic_ganadores(ganadores=winners)
    return schemaWinners


