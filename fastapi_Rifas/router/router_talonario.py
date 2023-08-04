from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.conexion import  get_db

from schema.schemas_Talonario import SchemaTalonario, TalonarioUpdate, SchemaTalonarioXBoleta, SchemaPostTalonario
from schema.schemas_Talonario import SchemaBoleta
from model.models import ModelTalonario, ModelBoleta
import model.models as models
import schema.schemas as schemas

from app.appBoletas import startCreateBoletas

routerTalonario = APIRouter()

@routerTalonario.get('/talonario/',response_model=List[SchemaTalonario])
def show_Talanario(db:Session=Depends(get_db)):
    talonarios = db.query(ModelTalonario).all()
    
    listaTalonario = []
    for talonario in talonarios:
        dictschema= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "fecha_Juego":talonario.fecha_Juego}
        schema_talonario= SchemaTalonario(**dictschema)
        listaTalonario.append(schema_talonario)
    return listaTalonario

@routerTalonario.get('/talonario/{talonario_id}',response_model=SchemaTalonarioXBoleta)
def show_boletas_Talonario(talonario_id:int,db:Session=Depends(get_db)):
    talonario = db.query(ModelTalonario).filter_by(id=talonario_id).first()
    listaBoletas= []
    for entrada in talonario.boletas:
        schemaboleta= SchemaBoleta(id = entrada.id, id_talonario= entrada.id_talonario, id_cliente = entrada.id_cliente, id_vendedor=entrada.id_vendedor, qr_code=entrada.qr_code, detalle=entrada.detalle, pagado=entrada.pagado, fecha_venta=entrada.fecha_venta)
        listaBoletas.append(schemaboleta)
    dictschema= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "fecha_Juego":talonario.fecha_Juego, "boletas": listaBoletas}
    schema_talonario= SchemaTalonarioXBoleta(**dictschema)

    return schema_talonario

@routerTalonario.post('/talonario/',response_model=SchemaPostTalonario)
def create_Talonario(entrada:SchemaPostTalonario, db:Session=Depends(get_db)):
    talonario = ModelTalonario(valor_boleta=entrada.valor_boleta, celular=entrada.celular, fecha_Juego=entrada.fecha_Juego, cantidad= entrada.cantidad)
    db.add(talonario)
    db.commit()
    db.refresh(talonario)
    
    startCreateBoletas(entrada.cantidad)

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
