from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_vendedor import *
from modelo.modelos import Vendedor

routerVendedor = APIRouter()


@routerVendedor.get("/vendedor", response_model= List[SchemaVendedorGet])
def obtener_cliente(db:Session =  Depends(get_db)):

  vendedores = db.query(Vendedor).all()
  schema_vendedores = []
  for vendedor in vendedores:
    #Se crea una instancia de SchemaVendedorGet y se pasa los atributos
    schema_vendedor = SchemaVendedorGet(id = vendedor.id, nombre=vendedor.nombre, apellido=vendedor.apellido, celular=vendedor.celular, correo = vendedor.correo)
    schema_vendedores.append(schema_vendedor)
  return schema_vendedores
  

  
@routerVendedor.post("/vendedor", response_model= SchemaVendedor)
def registrar_vendedor(vendedor:SchemaVendedorPost, db: Session = Depends(get_db)):
  respuesta = SchemaVendedor(mensaje=f"el vendedor {vendedor.nombre} se registro satisfactoria mente")
  nuevo_vendedor = Vendedor(nombre = vendedor.nombre, apellido = vendedor.apellido, celular = vendedor.celular, correo = vendedor.correo)
  db.add(nuevo_vendedor)
  db.commit()
  db.refresh(nuevo_vendedor)
  return respuesta
