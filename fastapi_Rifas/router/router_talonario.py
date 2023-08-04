from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from starlette.responses import RedirectResponse
from config.conexion import  get_db


from schema.schemas_Talonario import SchemaTalonario, TalonarioUpdate, SchemaTalonarioXBoleta, SchemaPostTalonario
from schema.schema_premios import SchemaPremios
from model.models import ModelTalonario, ModelPremio
import schema.schemas as schemas

from app.appBoletas import startCreateBoletas
from typing import List

import random

from .router_boletas import createBoletas, getListaBoletas
routerTalonario = APIRouter()

@routerTalonario.get('/talonario/',response_model=List[SchemaTalonario])
def show_Talanario(db:Session=Depends(get_db)):
    talonarios = db.query(ModelTalonario).all()
    
    listaTalonario = []
    for talonario in talonarios:
        dictschema= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad}
        schema_talonario= SchemaTalonario(**dictschema)
        listaTalonario.append(schema_talonario)
    return listaTalonario

@routerTalonario.get('/talonario/{talonario_id}',response_model=SchemaTalonarioXBoleta)
def show_boletas_Talonario(talonario_id:int,db:Session=Depends(get_db)):
    talonario = db.query(ModelTalonario).filter_by(id=talonario_id).first()

    listaBoletas= getListaBoletas(talonario)
    premios=[]
    for prem in talonario.premios:
        premio = SchemaPremios(id=prem.id, premio=prem.premio,imagen=prem.imagen, fecha_Juego=prem.fecha_Juego)
        premios.append(premio)
    dictschema= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad, "boletas": listaBoletas, "premios": premios}
    schema_talonario= SchemaTalonarioXBoleta(**dictschema)
    return schema_talonario



def generate_unique_six_digit_id():
    db=next(get_db())
    while True:
        six_digit_id = random.randint(100000, 9999990)
        if not db.query(ModelTalonario).filter_by(id=six_digit_id).first():
            return six_digit_id

@routerTalonario.post('/talonario/',response_model=SchemaPostTalonario)
def create_Talonario(entrada:SchemaPostTalonario, db:Session=Depends(get_db)):
    talonario = ModelTalonario(id = generate_unique_six_digit_id(), valor_boleta=entrada.valor_boleta, celular=entrada.celular, cantidad= entrada.cantidad)

    
    for prem in entrada.premios:
        premio = ModelPremio(premio = prem.premio, imagen= prem.imagen, fecha_Juego=prem.fecha_Juego, id_talonario=talonario.id)
        talonario.premios.append(premio)

    createBoletas(startCreateBoletas(entrada.cantidad), talonario, db)
    return entrada


@routerTalonario.put('/talonario/{talonario_id}',response_model=TalonarioUpdate)
def update_Talonario(talonario_id:int,entrada:TalonarioUpdate,db:Session=Depends(get_db)):
    talonario = db.query(ModelTalonario).filter_by(id=talonario_id).first()
    talonario.valor_boleta=entrada.valor_boleta
    talonario.celular=entrada.celular
    talonario.fecha_Juego=entrada.fecha_Juego
    db.commit()
    db.refresh(talonario)
    return talonario

@routerTalonario.delete('/talonario/{talonario_id}',response_model=schemas.Respuesta)
def delete_Talonario(boleta_id:int,db:Session=Depends(get_db)):
    boleta = db.query(ModelTalonario).filter_by(id=boleta_id).first()
    db.delete(boleta)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta
