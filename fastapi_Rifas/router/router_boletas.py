from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_boleta import SchemaBoleta, BoletaActualizar
from modelo.modelos import Boleta, Talonario, NumeroBoleta, id_seis_digitos
import random

routerBoletas = APIRouter()
"""

@routerBoletas.get("/")
def main():
    return RedirectResponse(url="/docs/")

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
def actualizar_Boleta(boleta_id:int, entrada:BoletaActualizar, db:Session=Depends(get_db)):
    
    boleta = db.query(Boleta).filter_by(id=boleta_id).first()
    
    boleta.id_vendedor=entrada.id_vendedor
    boleta.id_cliente=entrada.id_cliente
    boleta.qr_code=entrada.qr_code
    boleta.detalle=entrada.detalle
    boleta.pagado=entrada.pagado
    boleta.fecha_venta=entrada.fecha_venta
    db.commit()
    db.refresh(boleta)
    return boleta


def guardarBoletas(boletas, talonario, db):
    for boleta in boletas:
        boleta = Boleta(id = id_seis_digitos(),qr_code =boletas[boleta]["qr_code"])
        talonario.boletas.append(boleta)

        for numero in boletas[boleta]["numeros"]:
            numeros = NumeroBoleta(numero= numero, id_boleta=boleta.id)
            boleta.numeros.append(numeros)
    db.add(talonario)
    db.commit()
    db.refresh(talonario)

def darListaBoletas(talonario: Talonario):
    listaBoletas= []
    for boleta in talonario.boletas:
        listanumeros= []
        for num in boleta.numeros:
            listanumeros.append(num.numero)
        schemaboleta= SchemaBoleta(
            id = boleta.id, 
            id_talonario= boleta.id_talonario,
            qr_code=boleta.qr_code,
            estado_venta=boleta.estado_venta,
            estado_pagado=boleta.estado_pagado,
            numeros = listanumeros)
        listaBoletas.append(schemaboleta)
    return listaBoletas
"""
@routerBoletas.delete('/boletas/{boleta_id}',response_model=schemas.Respuesta)
def delete_boletas(boleta_id:int,db:Session=Depends(get_db)):
    boleta = db.query(ModelBoleta).filter_by(id=boleta_id).first()
    db.delete(boleta)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta
"""