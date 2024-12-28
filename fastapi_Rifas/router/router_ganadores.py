from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from schema.schema_ganador import *
from config.conexion import get_db
from sqlalchemy.orm import Session
from modelo.modelos import *

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
"""@routerGanadoras.post('/ganadores/{talonario_id}',response_model=SchemaGanador, tags=["Ganador"])
def registrar_numero_ganador(talonario_id:int,entrada:SchemaGanadorPost,db:Session=Depends(get_db)):
    Falta hacerlo

  
    return {}"""
@routerGanadoras.get('/talonario/{talonario_id}/{numeroGanador}/', tags=["Ganador"])
def Ganador_de_boleta(talonario_id: int, numeroGanador: str, db: Session = Depends(get_db)):
    # Busca el talonario por ID
    talonario = db.query(Talonario).filter(Talonario.id == talonario_id).first()
    if not talonario:
        raise HTTPException(status_code=404, detail="Talonario no encontrado")
    # Busca el dato en los boletas relacionadas

    resultado = (
    db.query(Boleta.id, Cliente.nombre, Cliente.celular, NumeroBoleta.numero, Boleta.estado_venta, Boleta.estado_pagado)
    .select_from(NumeroBoleta)  # Comenzar desde NumeroBoleta
    .join(Boleta, NumeroBoleta.id_boleta == Boleta.id)  # Relación explícita con Boleta
    .join(Cliente, Boleta.id_cliente == Cliente.id)  # Relación explícita con Cliente
    .filter(Boleta.id_talonario == talonario_id, NumeroBoleta.numero == numeroGanador)
    .all()
)


    print(resultado)

    if not resultado:
        raise HTTPException(status_code=404, detail="Dato no encontrado en este talonario")

    
    ganador = [
    SchemaGanador(
        id_boleta= id,
        nombre= nombre,
        celular= celular,
        numero_ganador= numero,
        estado_venta= estado_venta,
        estado_pagado= estado_pagado,
        estado_premio= "no me acuerdo que va aqui"
  
    )
    for id, nombre, celular, numero, estado_venta, estado_pagado in resultado
]

    return ganador

