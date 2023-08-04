from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from schema.schema_premios import *

from sqlalchemy.orm import Session

from config.conexion import get_db
from model.models import ModelTalonario


routerPremios = APIRouter()


@routerPremios.get("/juegos",response_model=List[Schema_info_Juegos])
def show_info_juegos(db:Session=Depends(get_db)):
    talonarios = db.query(ModelTalonario).all()
    listapremios=[] 
    for talonario in talonarios:
        for premio in talonario.premios:
            listapremios.append(premio)

    schem_info_juegos = []

    for actual in range(len(listapremios)):
        strpremios= []
        numganadores= []
        fecha1 = listapremios[actual].fecha_Juego.strftime("%Y-%m-%d")
        strpremios.append(listapremios[actual].premio)
        numganadores.append(listapremios[actual].ganador.numeroGanador)
        info_juegos=Schema_info_Juegos(dia=listapremios[actual].fecha_Juego.strftime("%A"), fecha= listapremios[actual].fecha_Juego, premio=strpremios, ganador = numganadores)
        for siguiente in range(actual + 1, len(listapremios) ):
            fecha2 = listapremios[siguiente].fecha_Juego.strftime("%Y-%m-%d")
            if fecha1 == fecha2:
                strpremios.append(listapremios[actual].premio)
                numganadores.append(listapremios[actual].ganador.numeroGanador)
                #listapremios.pop(siguiente)
        info_juegos.premio = strpremios
        info_juegos.ganador= numganadores
        schem_info_juegos.append(info_juegos)
    return schem_info_juegos
