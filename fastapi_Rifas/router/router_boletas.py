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


def id_consecutivo(id_talonario):
  db=next(get_db())
  cantidad = db.query(Boleta).filter_by(id_talonario=id_talonario).count()
  return cantidad + 1


def guardarBoletas(boletas, talonario, db):
    # por cada numero de boletas creo una instancia de Boletas y le ingreso la informacion
    db.add(talonario)
    db.commit()
    db.refresh(talonario)
    for boleta in boletas:
        nueva_boleta = Boleta(id = id_seis_digitos(),consecutiva_id = id_consecutivo(talonario.id), qr_code =boletas[boleta]["qr_code"])
        db.add(nueva_boleta)
        db.commit()
        db.refresh(nueva_boleta)

        # conmo tiene una relaionship se trata como una lista
        # un talonario tiene muchas boletas
        talonario.boletas.append(nueva_boleta)

        # De igual forma una boleta tiene muchos numeros de boletas,
        # se crea la instancia de NumeroBoleta y se le mete la informacion
        for numero in boletas[boleta]["numeros"]:
            numeros = NumeroBoleta(numero= numero, id_boleta=nueva_boleta.id)
            # Una boleta tiene muchos numeros
            nueva_boleta.numeros.append(numeros)

    # Se guarda en este caso solo talonario porque con el simple hecho de tener
    # una relationship ya todo queda empaquetado o relacionado (al hacer append)

    # un talonario tiene muchas boletas,
    # y una boleta tiene muchos numeros de boleta

    # Talonario -> Boleta -> NumeroBoleta
    
    # Talonario.boletas.append(Boleta)
    # Boleta.numerosBoletas.append(NumeroBoleta)
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