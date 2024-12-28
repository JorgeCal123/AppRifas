from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db
from schema.schema_talonario import *

from schema.schema_vendedor import *
from modelo.modelos import *
from fastapi import HTTPException
from functools import reduce
from sqlalchemy import func
from fastapi.responses import JSONResponse

routerVendedor = APIRouter()


@routerVendedor.post(
  "/vendedor",
  response_model= SchemaVendedor,
  tags=["Administrador-Vendedor"],
  summary="Registrar un Vendedor",
  description="Registra un vendedor para la venta de boletas")
def registrar_vendedor(vendedor:SchemaVendedorPost, db: Session = Depends(get_db)):
  nuevo_vendedor = Vendedor(cedula= vendedor.cedula, nombre = vendedor.nombre, apellido = vendedor.apellido, celular = vendedor.celular, correo = vendedor.correo)
  db.add(nuevo_vendedor)
  db.commit()
  db.refresh(nuevo_vendedor)
  
  vendedor = SchemaVendedor(mensaje=f"el vendedor {vendedor.nombre} se registro satisfactoria mente")
  return vendedor

@routerVendedor.get(
  "/vendedor",
  response_model= List[SchemaVendedorGet],
  tags=["Administrador-Vendedor"],
  summary="Mostrar todos los vendedores",
  description="Muestra una lista de todos los vendedores registrados"

)
def obtener_vendedor(db:Session =  Depends(get_db)):
  vendedores = db.query(Vendedor).all()
  schema_vendedores = []
  for vendedor in vendedores:
    #Se crea una instancia de SchemaVendedorGet y se pasa los atributos
    schema_vendedor = SchemaVendedorGet(cedula = vendedor.cedula, nombre=vendedor.nombre, apellido=vendedor.apellido, celular=vendedor.celular, correo = vendedor.correo)
    schema_vendedores.append(schema_vendedor)
  return schema_vendedores




@routerVendedor.put(
  "/vendedor/{cedula}",
  tags=["Administrador-Vendedor"],
  summary=" Modifica toda la informacion de un vendedor",
  description="Modifica un vendedor buscando su cedula"
)
def modificar_vendedor(vendedor:SchemaVendedorPut, cedula:str,  db: Session = Depends(get_db)):
  objeto_vendedor = db.query(Vendedor).filter_by(cedula = cedula).first()

  objeto_vendedor.cedula= vendedor.cedula
  objeto_vendedor.nombre = vendedor.nombre
  objeto_vendedor.apellido = vendedor.apellido
  objeto_vendedor.celular = vendedor.celular
  objeto_vendedor.correo = vendedor.correo

  db.commit()

  vendedor = SchemaVendedorGet(cedula=objeto_vendedor.cedula,
                                nombre=objeto_vendedor.nombre,
                                apellido=objeto_vendedor.apellido,
                                celular=objeto_vendedor.celular,
                                correo=objeto_vendedor.correo
                                )
  return vendedor

@routerVendedor.patch(
  "/vendedor/{cedula}",
  tags=["Administrador-Vendedor"],
  summary="Actualiza los campos necesarios de un vendedor",
  description="Actualiza un vendedor buscando la cedula"
  
)
def actualizar_vendedor(vendedor:SchemaVendedorPut, cedula:str,  db: Session = Depends(get_db)):
  
  objeto_vendedor = db.query(Vendedor).filter_by(cedula=cedula).first()
  if not objeto_vendedor:
    raise HTTPException(status_code=404, detail="Vendedor no encontrado")

  updates = vendedor.model_dump(exclude_unset=True)  # Excluir campos no enviados
  for key, value in updates.items():
    setattr(objeto_vendedor, key, value)

  db.commit()
  return {"mensaje": "actualizacion exitosa"}


@routerVendedor.delete(
  "/vendedor/{cedula}",
  tags=["Administrador-Vendedor"],
  summary="Eliminar Vendedor",
  description="Elimina un vendedor con la cedula"
)
def actualizar_vendedor(cedula:str,  db: Session = Depends(get_db)):
  vendedor = db.query(Vendedor).filter_by(cedula = cedula).first()
  db.delete(vendedor)
  db.commit()
  return {"mensaje": f"el vendedor con cedula {cedula} se ha eliminado"}

@routerVendedor.post(
  '/asignarboletasvendedor/{id_talonario}',
  response_model= List[SchemaBoletasAsignadas],
  tags=["Administrador-Vendedor"],
  summary="Asignar Boletas a un Vendedor",
  description="Asigna todas las boletas que deben tener los vendedores \n id_talonario: Es el id del talonario al que se va asignar las boletas \n entrada: vendedores con la cantidad de boletas asignadas \n Nota: Todas las boletas deben estar asignada a un vendedor, No puede haber boletas sin asignar"
)
def asignar_Boletas(id_talonario:int, entrada : List[SchemaCantidadBoletasVendedor], db:Session=Depends(get_db)):   
  total_asignada = reduce((lambda x, y: x + y.cantidad), entrada, 0)
  total = db.query(func.count(Boleta.id)).filter(Boleta.id_talonario == id_talonario).scalar()

  print(total_asignada)
  if total > total_asignada:
    raise HTTPException(status_code=400,
                        detail={"error": "Falta asignar Boletas","total": total,"total_asignada": total_asignada})
  elif total < total_asignada:
    raise HTTPException(status_code=400,
                        detail={"error":"Sobrepasa la cantidad de Boletas existentes","total": total,"total_asignada": total_asignada})
  else:
    # Falta asignale las boletas a los vendedores
    vendedores = []
    rango_inicial=1
    rango_final = 0
    for vendedor in entrada:
      rango_final = rango_final + vendedor.cantidad
      vendedor = db.query(Vendedor).filter_by(cedula = vendedor.cedula_vendedor).first()
      boletas = db.query(Boleta).filter(Boleta.consecutiva_id >= rango_inicial, Boleta.consecutiva_id <= rango_final, Boleta.id_talonario == id_talonario).all()
      vendedor.boletas.extend(boletas)
      rango_inicial = rango_final + 1
    db.commit()

    return JSONResponse(content={"mensaje": "Se asignaron las boletas a los vendedores"}, status_code=201)  




@routerVendedor.get(
  '/boletasAsignadasVendedores',
  tags=["Administrador-Vendedor"],
  summary=" Mostrar los Talonarios asignados de los Vendedores",
  description="Muestra Los talonarios y boletas asignados de cada uno de los vendedores"
)
def Boletas_Asignadas_Vendedor(db:Session=Depends(get_db)):
    # Consulta para obtener los vendedores y sus boletas agrupadas por talonario
    vendedores_con_boletas = (
        db.query(
            Vendedor.cedula,
            Vendedor.nombre,
            Boleta.id_talonario,
            func.group_concat(Boleta.id).label("boletas")
        )
        .join(Boleta, Boleta.id_vendedor == Vendedor.cedula)
        .group_by(Vendedor.cedula, Vendedor.nombre, Boleta.id_talonario)
        .all()
    )

    # Formatear el resultado_vendedor
    resultado_vendedor = {}
    for cedula, nombre, id_talonario, boletas in vendedores_con_boletas:
        if cedula not in resultado_vendedor:
            resultado_vendedor[cedula] = {
                "cedula": cedula,
                "nombre": nombre,
                "talonarios_asignados": []
            }
        resultado_Talonario={}
        if id_talonario not in resultado_Talonario:
          resultado_Talonario["talonario"] = {
            "id_talonario": id_talonario,
            "boletas": [int(boleta) for boleta in boletas.split(",")]
          }
        resultado_vendedor[cedula]["talonarios_asignados"].append(resultado_Talonario)

    return list(resultado_vendedor.values())


@routerVendedor.get(
  '/boletasAsignadasVendedor/{id_cedula}',
  tags=["Administrador-Vendedor"],
  summary="Mostrar talonario y boletas de un vendedor",
  description="Muestra el vendedores con id_cedula y los talonarios que se le asignaron"
)
def vendedores_talonario(id_cedula:str, db:Session=Depends(get_db)): 

  vendedor = db.query(Vendedor).filter_by(cedula = id_cedula).first()

  info_vendedot= {}
  info_vendedot["cedula"]=vendedor.cedula
  info_vendedot["nombre"]=vendedor.nombre
  for boleta in vendedor.boletas:
    if boleta.id_talonario not in info_vendedot:
      info_vendedot["talonario"] = {
        "id_talonario":boleta.id_talonario,
        "boletas": []}
      boletas= []

    info_boleta= {}
    info_boleta["id"]=boleta.id
    info_boleta["consecutive_id"]=boleta.consecutiva_id
    info_boleta["estado_venta"]=boleta.estado_venta
    info_boleta["estado_pagado"]=boleta.estado_pagado
    boletas.append(info_boleta)
    info_vendedot["talonario"]["boletas"]= boletas

     
  return info_vendedot