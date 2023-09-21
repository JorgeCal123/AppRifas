from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db
from datetime import datetime

from schema.schema_venta_boletas import *
from schema.schema_cliente import SchemaClienteGet
from modelo.modelos import Boleta, Cliente
routerVenta = APIRouter()


@routerVenta.patch("/venta_boletas{id_talonaro}", response_model= List[Schema_Boleta_vendida], tags=["Venta de Boletas"])
def registrar_venta_boleta(id_talonaro: int, vendidas:List[SchemaVenta], db: Session = Depends(get_db)):
  
  id_boletas = []  
  for boleta in vendidas:
    nuevo_venta = db.query(Boleta).filter_by(consecutiva_id = boleta.consecutiva_id, id_talonario=id_talonaro).first()
    nuevo_venta.estado_venta = True
    nuevo_venta.estado_pagado = boleta.pagada
    nuevo_venta.fecha_venta = datetime.now()
    boleta_vendida = Schema_Boleta_vendida(id=nuevo_venta.id)
    id_boletas.append(boleta_vendida)
    db.commit()
    db.refresh(nuevo_venta)
  return id_boletas


@routerVenta.get("/buscar_cliente/{celular}", response_model= List[SchemaClienteGet], tags=["Venta de Boletas"])
def buscar_usuario(celular:str, db: Session = Depends(get_db)):
  cliente = db.query(Cliente).filter(Cliente.celular.like(f"%{celular}%")).all()
  lista_clientes = []
  for datos in cliente:
    schema_cliente = SchemaClienteGet(
                                      id = datos.id,
                                      nombre = datos.nombre,
                                      apellido=datos.apellido,
                                      celular= datos.celular,
                                      direccion=datos.direccion,
                                      notificacion= datos.notificacion
                                      )
    lista_clientes.append(schema_cliente)
  return lista_clientes