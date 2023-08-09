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


@routerPremios.get("/juegos",response_model=List[SchemaInfoJuegos])
def mostrar_info_juegos(db:Session=Depends(get_db)):
 
    result = db.query(Premio.premio, Premio.fecha_juego, Ganador.numero_ganador) \
    .join(Ganador, Premio.id == Ganador.id_premio) \
    .filter(Premio.fecha_juego.between(obtener_fechas_lunes_a_domingo()["lunes"],  obtener_fechas_lunes_a_domingo()["domingo"])) \
    .all()
    print(result)
    print (obtener_fechas_lunes_a_domingo()["lunes"] + "  "+  obtener_fechas_lunes_a_domingo()["domingo"])

    response = []
    lista=["carro", "moto"]
    lista2=[2312, 4543]
    response.append(SchemaInfoJuegos(dia= "lunes",premio=lista,fecha= datetime.datetime.now(), ganador =lista2 ))
    return  response
