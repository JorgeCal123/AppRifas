from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, func, case, text, cast, Integer, String, Float
from schema.schema_venta_boletas import SchemaTalonarioVentasVendedor, SchemaVentasVendedor
from config.conexion import  get_db
from schema.schema_talonario import *
from schema.schema_vendedor import *
from modelo.modelos import *
from fastapi import HTTPException
from functools import reduce

from fastapi.responses import JSONResponse



routerAdmin= APIRouter()

  
  
 

"""
@routerAdmin.get(
  '/admin/boletasvendedor/{id_talonario}',
  response_model= SchemaTalonarioXvendedor, 
  tags=["Administrador"],
  summary="",
  description=""
)
def talonario_vendedor(id_talonario:int, db:Session=Depends(get_db)): 

  
  datos_talonario = db.query(Talonario.id, Talonario.cantidad).filter_by(id = id_talonario).first()
  print(datos_talonario)
  
  vendedores = db.query(Vendedor.cedula, Vendedor.nombre, Vendedor.apellido)
  lista_vendedores = []
  for vendedor in vendedores:
    nombre = vendedor.nombre + ' '+ vendedor.apellido
    schema_vendedor = SchemaInfoVendedor(id = vendedor.cedula, nombre = nombre)
    lista_vendedores.append(schema_vendedor)
  
  vendedor = SchemaTalonarioXvendedor(id_talonario = datos_talonario.id, cantidad = datos_talonario.cantidad, vendedores =  lista_vendedores)
  
  return vendedor
"""



@routerAdmin.post(
  '/config/porcentajeremuneracion/',
  tags=["Administrador"],
  summary="Asigna el porentaje que se le paga a un vendedor",
  description=""
  )
def Boletas_asignadas(entrada : List[SchemaPorcentajeVendedor], db:Session=Depends(get_db)):
  for remuneracion in entrada:
    porcentaje = RemuneracionVendedor(**remuneracion.model_dump())
    db.add(porcentaje)
    db.commit()
    db.refresh(porcentaje)
  return entrada
"""
[
  {
    "valor_boleta": "2000",
    "porcentaje": 30
  },
  {
    "valor_boleta": 3000,
    "porcentaje": 30
  },
  {
    "valor_boleta": 5000,
    "porcentaje": 25
  },
  {
    "valor_boleta": 10000,
    "porcentaje": 30
  },
  {
    "valor_boleta": 20000,
    "porcentaje": 30
  }
]
"""

@routerAdmin.patch(
  "/config/porcentajeremuneracion/",
  tags=["Administrador"],
  summary="",
  description=""
)
def actualizar_vendedor(vendedor:SchemaPorcentajeVendedor, db: Session = Depends(get_db)):
  db.query(RemuneracionVendedor).filter_by(valor_boleta = vendedor.valor_boleta).update(vendedor.model_dump())
  db.commit()
  return vendedor.model_dump()

@routerAdmin.get("/ventas/vendedor/", tags=["Administrador"],summary="Informacion de las ventas de cada uno de los vendedores por talonario")
def ventas_vendedor(db: Session = Depends(get_db)):
  ventas = db.query(
    Talonario.id.label('id_talonario'),
    Premio.fecha_juego.label('fecha_juego'),
    Vendedor.cedula.label('cedula'),
    Vendedor.nombre.label('nombre_vendedor'),
    func.count(Boleta.id).label('cantidad_asignada'),
    func.sum(case((Boleta.estado_venta == True, 1), else_=0)).label('cantidad_vendidas'),
    Talonario.valor_boleta.label('precio'),
    func.sum(case((Boleta.estado_venta == True, Talonario.valor_boleta), else_=0)).label('total_venta'),
    cast(func.sum(case((Boleta.estado_venta == True, Talonario.valor_boleta), else_=0)) *
    (RemuneracionVendedor.porcentaje / 100), Integer).label('pago'),
    func.concat(cast(func.min(Boleta.consecutiva_id), String), ' - ', cast(func.max(Boleta.consecutiva_id), String)).label('rango')
).join(Vendedor, Vendedor.cedula == Boleta.id_vendedor).join(Talonario, Talonario.id ==   Boleta.id_talonario, isouter=True).join(RemuneracionVendedor, RemuneracionVendedor.valor_boleta == Talonario.valor_boleta).join(Premio, Premio.id_talonario == Talonario.id).group_by(Talonario.id, Vendedor.cedula)
  #fecha=juegos.fecha_juego.strftime("%d-%m-%Y")
  resultado_esquemas = {}
  for row in ventas.all():
    ventas_vendedor = SchemaVentasVendedor(
        nombre_vendedor=row.nombre_vendedor,
        cantidad_boletas_asignadas=row.cantidad_asignada,
        cantidad_boletas_vendidas=row.cantidad_vendidas,
        precio_unitario=row.precio,
        total_ventas=row.total_venta,
        pago=row.pago,
        rango_asignado=row.rango
    )

    talonario_id = row.id_talonario
    fecha_juego = row.fecha_juego.strftime("%d-%m-%Y")

    if talonario_id in resultado_esquemas:
        resultado_esquemas[talonario_id].ventas_vendedor.append(ventas_vendedor)
    else:
        talonario_ventas = SchemaTalonarioVentasVendedor(
            talonario_id=talonario_id,
            fecha_juego=fecha_juego,
            ventas_vendedor=[ventas_vendedor]
        )
        resultado_esquemas[talonario_id] = talonario_ventas

  resultado_final = list(resultado_esquemas.values())
  return resultado_final
