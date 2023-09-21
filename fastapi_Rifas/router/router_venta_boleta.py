from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_venta_boletas import *
from schema.schema_cliente import SchemaClienteGet
from modelo.modelos import Boleta, Cliente
routerVendedor = APIRouter()


@routerVendedor.patch("/venta-boleta", response_model= list[Schema_Boleta_vendida])
def registrar_boleta_vendida(vendidas:SchemaVenta, db: Session = Depends(get_db)):
  
  # respuesta = SchemaVendedor(mensaje=f"el vendedor {vendedor.nombre} se registro satisfactoria mente")

  id_boletas = []  
  for boleta in vendidas:
    nuevo_venta = db.query(Boleta).filter_by(consecutivo_id = boleta.consecutivo_id).first()
    nuevo_venta.estado_venta = True
    nuevo_venta.estado_pagado = boleta.pagada
    boleta_vendida = Schema_Boleta_vendida(nuevo_venta.id)
    id_boletas.append(boleta_vendida)
    db.commit()
    db.refresh(nuevo_venta)
  return id_boletas


@routerVendedor.GET("/cliente-existe/{celular}", response_model= list[SchemaClienteGet])
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