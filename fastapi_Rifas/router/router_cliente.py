from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_cliente import SchemaBoleta, SchemaCliente, SchemaClientePost, SchemaClienteGet, SchemaClienteBasic, SchemaClientePatch
from schema.schema_venta_boletas import Schema_Boleta_vendida, SchemaClienteBoletas
from modelo.modelos import Cliente, Boleta
import datetime
from sqlalchemy.orm import sessionmaker

routerCliente = APIRouter()


@routerCliente.get("/cliente/", response_model= List[SchemaClienteBasic], tags=["Cliente"])
def obtener_clientes(db:Session =  Depends(get_db)):

  clientes = db.query(Cliente).all()
  schema_clientes = []
  for cliente in clientes:
    #Se crea una instancia de SchemaClienteGet y se pasa los atributos
    schema_cliente = SchemaClienteBasic(id = cliente.id, nombre=cliente.nombre, apellido=cliente.apellido, celular=cliente.celular, direccion=cliente.direccion, notificacion=cliente.notificacion)
    schema_clientes.append(schema_cliente)
  return schema_clientes
  

  
@routerCliente.post("/cliente/", response_model= SchemaCliente, tags=["Cliente"])
def registrar_cliente(cliente:SchemaClientePost, db: Session = Depends(get_db)):
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} se registro satisfactoria mente")
  nuevo_cliente = Cliente(nombre = cliente.nombre, apellido = cliente.apellido, celular = cliente.celular, direccion = cliente.direccion, notificacion = cliente.notificacion)
  db.add(nuevo_cliente)
  db.commit()
  db.refresh(nuevo_cliente)
  return respuesta




@routerCliente.patch("/cliente/{id_cliente}", response_model= SchemaCliente, tags=["Cliente"])
def registrar_boletas(id_cliente:int, boletas_vendidas: List[Schema_Boleta_vendida], db: Session = Depends(get_db)):

  cliente = db.query(Cliente).filter_by(id = id_cliente).first()
  for id_boleta in boletas_vendidas:
    boleta = db.query(Boleta).filter_by(id=id_boleta.id).first()
    cliente.boletas.append(boleta)
  db.commit()
  db.refresh(cliente)
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} se vendieron las boletas")
  return respuesta

@routerCliente.get("/cliente/{celular}",
                   response_model= List[SchemaClienteGet],
                   tags=["Cliente"],
                   summary="Buscar cliente con numero Celular")
def buscar_usuario(celular:str, db: Session = Depends(get_db)):
  cliente = db.query(Cliente).filter(Cliente.celular.like(f"%{celular}%")).all()
  lista_clientes = []


  for datos in cliente:
    schema_Boleta  = getSchemaBoleta(cliente = datos.id, db=db)
    schema_cliente = SchemaClienteGet(
                                      id = datos.id,
                                      nombre = datos.nombre,
                                      apellido=datos.apellido,
                                      celular= datos.celular,
                                      direccion=datos.direccion,
                                      notificacion= datos.notificacion,
                                      boletas = schema_Boleta
                                      )
    lista_clientes.append(schema_cliente)
  return lista_clientes


def getSchemaBoleta(cliente, db):
    boletas = db.query(Boleta).filter_by(id_cliente = cliente).all()
    schema_Boletas = []
    for boleta in boletas:
      numeros = []
      for numero_boleta in boleta.numeros:
        numeros.append(numero_boleta.numero)

      schema_boleta = SchemaBoleta(fecha=boleta.fecha_venta.strftime("%d-%m-%Y"),
                                   conscutive_id=str(boleta.consecutiva_id),
                                   oportunidades=numeros,
                                   nombre_vendedor=boleta.vendedor.nombre,
                                   estado_pago=boleta.estado_pagado)
      schema_Boletas.append(schema_boleta)
    return schema_Boletas
  
  
@routerCliente.put("/cliente/{celular}",
                   tags=["Cliente"],
                   summary="Actualizar cliente con numero Celular xd")
def actualizar_usuario(celular:str, entrada: SchemaClientePatch, db: Session = Depends(get_db)):
  cliente = db.query(Cliente).filter_by(celular = celular).first()
  if not cliente:
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

  if entrada.nombre is not None:
    cliente.nombre = entrada.nombre
  if entrada.apellido is not None:
    cliente.apellido = entrada.apellido
  if entrada.celular is not None:
    cliente.celular = entrada.celular
  if entrada.direccion is not None:
    cliente.direccion = entrada.direccion
  if entrada.notificacion is not None:
    cliente.notificacion = entrada.notificacion
  
  cliente_actualizado = SchemaClienteGet(id=cliente.id,
                                         nombre=cliente.nombre,
                                         apellido=cliente.apellido,
                                         celular= cliente.celular,
                                         direccion= cliente.direccion,
                                         notificacion=cliente.notificacion,
                                         boletas=getSchemaBoleta(cliente.id, db))

  return cliente_actualizado