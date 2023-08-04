from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from config.conexion import  get_db

from schema.schemas_cliente import SchemaCliente, SchemaClientePost
from model.models import ModelCliente
import schema.schemas as schemas
import pprint
import random

routerCliente = APIRouter()


@routerCliente.post("/cliente/", response_model= SchemaCliente)
def crear_cliente(cliente:SchemaClientePost, db: Session = Depends(get_db)):
  respuesta = SchemaCliente(mensaje=f"el cliente {cliente.nombre} se registro satisfactoria mente")
  nuevo_cliente = ModelCliente(nombre = cliente.nombre, apellido = cliente.apellido, celular = cliente.celular, direccion = cliente.direccion, notificacion = cliente.notificacion)
  db.add(nuevo_cliente)
  db.commit()
  db.refresh(nuevo_cliente)
  return respuesta
  