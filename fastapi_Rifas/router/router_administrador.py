from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc
from config.conexion import  get_db
from schema.schema_talonario import *
from schema.schema_vendedor import *
from modelo.modelos import *
from fastapi import HTTPException
from functools import reduce



routerAdmin= APIRouter()


@routerAdmin.get('/admin/opcionestalonario',response_model=List[SchemaTalonarioXpremio])
def opciones_talonarios(db:Session=Depends(get_db)):
  
  """
    La función `opciones_talonario` recupera información sobre premios y números de boletos de una base de datos  y devuelve una lista de objetos `SchemaTalonarioXpremio`.
    
    param db: El parámetro `db` es de tipo `Session` y se utiliza para acceder a la base de datos. Se obtiene
    obtiene utilizando la función `Depends` con la función `get_db` como dependencia. La función `get_db`
    se encarga de crear una nueva sesión de base de datos y devolverla
    :tipo db: Sesión
    :return: una lista de objetos de tipo `EsquemaTalonarioXpremio`.
  """
  
  info_premio = db.query(Talonario.id, Premio.premio, Premio.fecha_juego).join(Premio, Talonario.id == Premio.id_talonario).all()
  print(info_premio)
  formato_info_premio = talonarios_premio(info_premio)
  lista_talonarioXpremio = []
  
  for k, v in formato_info_premio.items():
    talonarioXpremio = SchemaTalonarioXpremio(id_talonario=k, premios = v)
    lista_talonarioXpremio.append(talonarioXpremio)
  
  return lista_talonarioXpremio
  
  
  
def talonarios_premio(info_premio): 
  """
  La función `talonarios_premio` toma una lista de objetos `info_premio` y devuelve un diccionario donde las claves son el atributo `id` de cada objeto `info_premio` y los valores son listas de objetos
  objetos `SchemaInfopremio` que contienen los atributos `premio` y `fecha_juego` de cada objeto de cada objeto `info_premio`.
  
  * param info_premio: El parámetro `info_premio` es una lista de objetos que contienen
    información sobrepremios.
  
  *return: un diccionario donde las claves son los ID de los premios y los valores son listas de objetos EsquemaInfopremio.
  """
  
  dict_premio = {}
  for premio in info_premio:
    fecha_premio = premio.fecha_juego.strftime("%d-%m-%Y")
    if premio.id not in dict_premio:
      premio_lista = []
      juego = SchemaInfopremio(premio = premio.premio, fecha = fecha_premio)
      premio_lista.append(juego)
      dict_premio[premio.id] = premio_lista
    else:
      lista_nueva_premios= dict_premio.get(premio.id)
      juego = SchemaInfopremio(premio = premio.premio, fecha = fecha_premio)
      lista_nueva_premios.append(juego)
      dict_premio[premio.id] = lista_nueva_premios
  return dict_premio



@routerAdmin.get('/admin/boletasvendedor/{id_talonario}', response_model= SchemaTalonarioXvendedor)
def talonario_vendedor(id_talonario:int, db:Session=Depends(get_db)): 

  
  datos_talonario = db.query(Talonario.id, Talonario.cantidad).filter_by(id = id_talonario).first()
  print(datos_talonario)
  
  vendedores = db.query(Vendedor.id, Vendedor.nombre, Vendedor.apellido)
  lista_vendedores = []
  for vendedor in vendedores:
    nombre = vendedor.nombre + ' '+ vendedor.apellido
    schema_vendedor = SchemaInfoVendedor(id = vendedor.id, nombre = nombre)
    lista_vendedores.append(schema_vendedor)
  
  vendedor = SchemaTalonarioXvendedor(id_talonario = datos_talonario.id, cantidad = datos_talonario.cantidad, vendedores =  lista_vendedores)
  
  return vendedor



@routerAdmin.post('/admin/cantidadboletasvendedor/{id_talonario}', response_model= List[SchemaBoletasAsignadas])
def Boletas_asignadas(id_talonario:int, total : int, entrada : List[SchemaCantidadBoletasVendedor], db:Session=Depends(get_db)):   
  total_asignada = reduce((lambda x, y: x + y.cantidad), entrada, 0)
  print(total_asignada)
  if total > total_asignada:
    raise HTTPException(status_code=400, detail="Falta asignar Boletas")
  elif total < total_asignada:
    raise HTTPException(status_code=400, detail="Sobrepasa la cantidad de Boletas existentes")
  else:
    # Falta asignale las boletas a los vendedores
    vendedores = []
    rango_inicial=1
    rango_final = 0
    for vendedor in entrada:
      rango_final = rango_final + vendedor.cantidad
      nombre_vendedor = db.query(Vendedor.nombre).filter_by(id = vendedor.id_vendedor).first()
      vendedor = SchemaBoletasAsignadas(id_vendedor=vendedor.id_vendedor, nombre=nombre_vendedor[0],rango_inicial=rango_inicial, rango_final=rango_final)
      vendedores.append(vendedor)
      rango_inicial = rango_final + 1
    guardar_boletas_vendedor(id_talonario, vendedores, db)
    return vendedores

def guardar_boletas_vendedor(id_talonario, vendedores, db):
    boletas_talonario = db.query(Boleta).filter_by(id_talonario = id_talonario).order_by(asc(Boleta.consecutiva_id)).all()
    for vendedor_schema in vendedores:
      vendedor = db.query(Vendedor).filter_by(id = vendedor_schema.id_vendedor).first()
      for consecutive_id in range(vendedor_schema.rango_inicial - 1, vendedor_schema.rango_final):
        print(consecutive_id)
        vendedor.boletas.append(boletas_talonario[consecutive_id])
    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)










