from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db
import datetime

from schema.schema_venta_boletas import *
from schema.schema_cliente import SchemaCliente
from modelo.modelos import Boleta, Cliente

routerVenta = APIRouter()


@routerVenta.patch("/venta_boletas{id_talonaro}", response_model= List[Schema_Boleta_vendida], tags=["Venta de Boletas"])
def registrar_venta_boleta(id_talonaro: int, vendidas:List[SchemaVenta], db: Session = Depends(get_db)):
  
  id_boletas = []  
  for boleta in vendidas:
    nuevo_venta = db.query(Boleta).filter_by(consecutiva_id = boleta.consecutiva_id, id_talonario=id_talonaro).first()
    nuevo_venta.estado_venta = True
    nuevo_venta.estado_pagado = boleta.pagada
    nuevo_venta.fecha_venta = datetime.datetime.now()
    boleta_vendida = Schema_Boleta_vendida(id=nuevo_venta.id)
    id_boletas.append(boleta_vendida)
    db.commit()
    db.refresh(nuevo_venta)
  return id_boletas

@routerVenta.post("/cliente/boletas/", response_model= SchemaCliente, tags=["Venta de Boletas"])
def registro_cliente_venta_boletas(cliente:SchemaClienteBoletas, id_talonario:int, db: Session = Depends(get_db)):

  nuevo_cliente = Cliente(nombre = cliente.nombre, apellido = cliente.apellido, celular = cliente.celular, direccion = cliente.direccion, notificacion = cliente.notificacion)
  for venta_boleta in cliente.venta_boletas:
    boleta = db.query(Boleta).filter(Boleta.consecutiva_id == venta_boleta.consecutiva_id, Boleta.id_talonario == id_talonario).first()
    print(venta_boleta.consecutiva_id)
    if boleta:
      boleta.estado_venta = True
      boleta.estado_pagado = venta_boleta.pagada
      boleta.fecha_venta = datetime.datetime.now()

    nuevo_cliente.boletas.append(boleta)

  db.add(nuevo_cliente)
  db.commit()
  db.refresh(nuevo_cliente)
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} registro y venta satisfactoria")
  return respuesta


@routerVenta.get("/vendedor/boletas/", response_model= List[SchemaTalonarioVentasVendedor], tags=["Venta de Boletas"])
def reporte_venta_boletas(db: Session = Depends(get_db)):


  """
  select vendedor.nombre, boleta.estado_venta, talonario.valor_boleta, talonario.id, vendedor.cedula, premio.premio  
  on id_vendedor= vendedor.cedula
  """