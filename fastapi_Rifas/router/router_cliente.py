from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_cliente import SchemaCliente, SchemaClientePost, SchemaClienteGet, SchemaClienteBoletas
from schema.schema_venta_boletas import Schema_Boleta_vendida
from modelo.modelos import Cliente, Boleta

routerCliente = APIRouter()


@routerCliente.get("/cliente/", response_model= List[SchemaClienteGet], tags=["Cliente"])
def obtener_cliente(db:Session =  Depends(get_db)):

  clientes = db.query(Cliente).all()
  schema_clientes = []
  for cliente in clientes:
    #Se crea una instancia de SchemaClienteGet y se pasa los atributos
    schema_cliente = SchemaClienteGet(id = cliente.id, nombre=cliente.nombre, apellido=cliente.apellido, celular=cliente.celular, direccion=cliente.direccion, notificacion=cliente.notificacion)
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


@routerCliente.post("/cliente/boletas/", response_model= SchemaCliente, tags=["Cliente"])
def registrar_cliente_boletas(cliente:SchemaClienteBoletas, db: Session = Depends(get_db)):

  nuevo_cliente = Cliente(nombre = cliente.nombre, apellido = cliente.apellido, celular = cliente.celular, direccion = cliente.direccion, notificacion = cliente.notificacion)
  for id_boleta in cliente.id_boletas:
    boleta = db.query(Boleta).filter_by(id=id_boleta.id).first()
    nuevo_cliente.boletas.append(boleta)
  db.add(nuevo_cliente)
  db.commit()
  db.refresh(nuevo_cliente)
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} registro y venta satisfactoria")
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