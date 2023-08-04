from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.conexion import  get_db

from schema.schemas_boleta import SchemaBoleta, BoletaUpdate
from model.models import ModelBoleta, ModelTalonario
import model.models as models
import schema.schemas as schemas


routerBoletas = APIRouter()

@routerBoletas.get("/")
def main():
    return RedirectResponse(url="/docs/")

"""
@routerBoletas.get('/boletas/',response_model=List[SchemaBoleta])
def show_boletas(db:Session=Depends(get_db)):
    usuarios = db.query(ModelBoleta).all()
    return usuarios

@routerBoletas.post('/boletas/',response_model=SchemaBoleta)
def create_boletas(entrada:SchemaBoleta, db:Session=Depends(get_db)):
    talonario = db.query(ModelTalonario).filter_by(id=entrada.id_talonario).first()
    boleta = ModelBoleta(id_cliente = entrada.id_cliente, id_vendedor=entrada.id_vendedor, qr_code=entrada.qr_code, detalle=entrada.detalle, pagado=entrada.pagado, fecha_venta=entrada.fecha_venta)
    talonario.boletas.append(boleta)
    db.commit()
    db.refresh(talonario)
    return boleta
"""
@routerBoletas.put('/boletas/{boleta_id}',response_model=SchemaBoleta)
def update_Boleta(boleta_id:int,entrada:BoletaUpdate,db:Session=Depends(get_db)):
    boleta = db.query(ModelBoleta).filter_by(id=boleta_id).first()
    boleta.id_vendedor=entrada.id_vendedor
    boleta.id_cliente=entrada.id_cliente
    boleta.qr_code=entrada.qr_code
    boleta.detalle=entrada.detalle
    boleta.pagado=entrada.pagado
    boleta.fecha_venta=entrada.fecha_venta
    db.commit()
    db.refresh(boleta)
    return boleta
"""
@routerBoletas.delete('/boletas/{boleta_id}',response_model=schemas.Respuesta)
def delete_boletas(boleta_id:int,db:Session=Depends(get_db)):
    boleta = db.query(ModelBoleta).filter_by(id=boleta_id).first()
    db.delete(boleta)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta
"""