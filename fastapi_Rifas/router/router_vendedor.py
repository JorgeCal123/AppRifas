from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db

from schema.schema_vendedor import *
from modelo.modelos import Vendedor, RemuneracionVendedor

routerVendedor = APIRouter()


@routerVendedor.get("/vendedor", response_model= List[SchemaVendedorGet], tags=["Vendedor"])
def obtener_vendedor(db:Session =  Depends(get_db)):

  vendedores = db.query(Vendedor).all()
  schema_vendedores = []
  for vendedor in vendedores:
    #Se crea una instancia de SchemaVendedorGet y se pasa los atributos
    schema_vendedor = SchemaVendedorGet(cedula = vendedor.cedula, nombre=vendedor.nombre, apellido=vendedor.apellido, celular=vendedor.celular, correo = vendedor.correo)
    schema_vendedores.append(schema_vendedor)
  return schema_vendedores
  

  
@routerVendedor.post("/vendedor", response_model= SchemaVendedor, tags=["Vendedor"])
def registrar_vendedor(vendedor:SchemaVendedorPost, db: Session = Depends(get_db)):
  respuesta = SchemaVendedor(mensaje=f"el vendedor {vendedor.nombre} se registro satisfactoria mente")
  nuevo_vendedor = Vendedor(cedula= vendedor.cedula, nombre = vendedor.nombre, apellido = vendedor.apellido, celular = vendedor.celular, correo = vendedor.correo)
  db.add(nuevo_vendedor)
  db.commit()
  db.refresh(nuevo_vendedor)
  return respuesta


@routerVendedor.put("/vendedor/{cedula}", tags=["Vendedor"])
def actualizar_vendedor(vendedor:SchemaVendedorPut, cedula:str,  db: Session = Depends(get_db)):
  objeto_vendedor = db.query(Vendedor).filter_by(cedula = cedula).first()
  if vendedor.cedula is not None:
    objeto_vendedor.cedula= vendedor.cedula
  if vendedor.nombre is not None:
    objeto_vendedor.nombre = vendedor.nombre
  if vendedor.apellido is not None:
    objeto_vendedor.apellido = vendedor.apellido
  if vendedor.celular is not None:
    objeto_vendedor.celular = vendedor.celular
  if vendedor.correo is not None:
    objeto_vendedor.correo = vendedor.correo
  db.commit()
  respuesta = SchemaVendedorGet(cedula=objeto_vendedor.cedula,
                                nombre=objeto_vendedor.nombre,
                                apellido=objeto_vendedor.apellido,
                                celular=objeto_vendedor.celular,
                                correo=objeto_vendedor.correo
                                )
  return respuesta

@routerVendedor.patch("/vendedor/{cedula}", tags=["Vendedor"])
def actualizar_vendedor(vendedor:SchemaVendedorPut, cedula:str,  db: Session = Depends(get_db)):
  db.query(RemuneracionVendedor).filter_by(valor_boleta = cedula).update(vendedor.model_dump(exclude_unset=True))
  db.commit()
  return {"mensaje": "sea actualizo"}


@routerVendedor.delete("/vendedor/{cedula}", tags=["Vendedor"])
def actualizar_vendedor(cedula:str,  db: Session = Depends(get_db)):
  vendedor = db.query(Vendedor).filter_by(cedula = cedula).first()
  db.delete(vendedor)
  db.commit()
  return {"mensaje": f"el vendedor con cedula {cedula} se ha eliminado"}
