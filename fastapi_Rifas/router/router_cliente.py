from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.conexion import  get_db

from schema.schemas_cliente import SchemaCliente, SchemaClientePost, SchemaClienteGet
from model.models import ModelCliente
import schema.schemas as schemas
import pprint
import random

routerCliente = APIRouter()


@routerCliente.get("/cliente", response_model= List[SchemaClienteGet])
def obtener_cliente(db:Session =  Depends(get_db)):

  clientes = db.query(ModelCliente).all()
  schema_clientes = []
  for cliente in clientes:
    #Se crea una instancia de SchemaClienteGet y se pasa los atributos
    schema_cliente = SchemaClienteGet(id = cliente.id, nombre=cliente.nombre, apellido=cliente.apellido, celular=cliente.celular, direccion=cliente.direccion, notificacion=cliente.notificacion)
    schema_clientes.append(schema_cliente)
  return schema_clientes
  

  
@routerCliente.post("/cliente/", response_model= SchemaCliente)
def crear_cliente(cliente:SchemaClientePost, db: Session = Depends(get_db)):
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} se registro satisfactoria mente")
  nuevo_cliente = ModelCliente(nombre = cliente.nombre, apellido = cliente.apellido, celular = cliente.celular, direccion = cliente.direccion, notificacion = cliente.notificacion)
  db.add(nuevo_cliente)
  db.commit()
  db.refresh(nuevo_cliente)
  return respuesta
  