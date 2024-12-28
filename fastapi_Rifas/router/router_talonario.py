from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from schema.schema_talonario import *

from config.conexion import  get_db

from schema.schema_talonario import SchemaTalonario, SchemaTalonarioPut, SchemaTalonarioXBoleta, SchemaTalonarioPost, SchemaInfopremio
from schema.schema_premios import SchemaPremios
from modelo.modelos import Talonario, Premio, id_seis_digitos
import schema.schemas as schemas

from typing import List

from .router_boletas import guardarBoletas, darListaBoletas

from fastapi.responses import JSONResponse

routerTalonario = APIRouter()


@routerTalonario.post(
    '/talonario/',
    tags=["Administador-Talonario"],
    summary="Crear un talonario",
    description="Crea un talonario, las boletas y los premios"
)
def crear_Talonario(entrada:SchemaTalonarioPost, db:Session=Depends(get_db)):

    if int(entrada.cantidad_oportunidades) not in [2, 3, 8, 10]:
        raise HTTPException(
            status_code=400,
            detail="la cantidad_oportunidades solo puede ingresar valores 2, 3, 8 o 10"
        )
    talonario = Talonario(id = id_seis_digitos(), valor_boleta=entrada.valor_boleta, celular=entrada.celular, cantidad= entrada.cantidad_Boletas)

    for premio in entrada.premios:
        nuevo_premio = Premio(premio = premio.premio, imagen= premio.imagen, fecha_juego=premio.fecha_juego, id_talonario=talonario.id)
        talonario.premios.append(nuevo_premio)

    guardarBoletas(entrada.cantidad_Boletas, entrada.cantidad_oportunidades, talonario, db)
    data = {"mensaje": "¡Operación exitosa!", "Id_talonario": talonario.id}
    return JSONResponse(content=data, status_code=201)  



@routerTalonario.get(
    '/admin/consultar-talonario-premios',
    response_model=List[SchemaTalonarioXpremio],
    tags=["Administador-Talonario"],
    summary="Consulta todos los premios que se rifan en cada talonario (Modificar a que busque los premios de un talonario en especifico)",
    description="Esta API devuelve una lista de premios con su respectiva fecha asociados a cada talonario con su id."
)
def consultar_talonario_por_premios(db:Session=Depends(get_db)):
  try:
    info_premio = (
      db.query(Talonario.id, Premio.premio, Premio.fecha_juego)
      .join(Premio, Talonario.id == Premio.id_talonario)
      .all()
    )

    if not info_premio:
      raise HTTPException(
      status_code=404,
      detail="No se encontraron premios asociados a talonarios."
    )

    formato_info_premio = talonarios_premio(info_premio)
    lista_talonarioXpremio = []
    
    for k, v in formato_info_premio.items():
      talonarioXpremio = SchemaTalonarioXpremio(id_talonario=k, premios = v)
      lista_talonarioXpremio.append(talonarioXpremio)
    
    return lista_talonarioXpremio

  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"Ocurrió un error inesperado: {str(e)}"
    )
  
   
def talonarios_premio(info_premio): 
  """
  La función `talonarios_premio` toma una lista de objetos `info_premio` y devuelve un diccionario donde las claves son el atributo `id` de cada objeto `info_premio` y los valores son listas de objetos
  objetos `SchemaInfopremio` que contienen los atributos `premio` y `fecha_juego` de cada objeto de cada objeto `info_premio`.
  
  * param info_premio: El parámetro `info_premio` es una lista de objetos que contienen
    información sobre premios.
  
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


@routerTalonario.get(
        '/talonario/',
        response_model=List[SchemaTalonario],
        tags=["Administador-Talonario"],
        summary="Mostrar el talanario y sus premios",
        description="Muesta la informacion basica de todos los Talonarios y los premios que esta premiando sus respectivo talonario"
)
def mostrar_Talanario_General(db:Session=Depends(get_db)):
    talonarios = db.query(Talonario).all()
    
    lista_talonario = []
    for talonario in talonarios:
        premios=[]
        for premio in talonario.premios:
            fecha_formateada = premio.fecha_juego.strftime("%d/%b/%Y")

            datos_premio= {"premio": premio.premio, "fecha": fecha_formateada}
            schemapremio=SchemaInfopremio(**datos_premio)
            premios.append(schemapremio)
        datos_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad, "infopremio": premios}
        schema_talonario= SchemaTalonario(**datos_talonario)
        lista_talonario.append(schema_talonario)
    return lista_talonario

@routerTalonario.get(
    '/talonario/{talonario_id}',
    response_model=SchemaTalonarioXBoleta,
    tags=["Administador-Talonario"],
    summary="Buscar Talanario (Talonario X Boletas X Premios)",
    description="Muestra toda la informacion de un talonario\n",
    
)
def mostrar_Talonario_Completo(talonario_id:int,db:Session=Depends(get_db)):
    """
    ### parameters:
    - **talonario_id** id del talonario que quiere consultar"""
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()

    lista_boletas= darListaBoletas(talonario)
    premios=[]
    for prem in talonario.premios:
        premio = SchemaPremios(id=prem.id, premio=prem.premio, imagen=prem.imagen, fecha_juego=prem.fecha_juego)
        premios.append(premio)
    schema_premio_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad, "boletas": lista_boletas, "premios": premios}
    schema_talonario= SchemaTalonarioXBoleta(**schema_premio_talonario)
    return schema_talonario


@routerTalonario.put(
    '/talonario/{talonario_id}',
    response_model=SchemaTalonarioPut,
    tags=["Administador-Talonario"]
)
def actualizar_Talonario(talonario_id:int,entrada:SchemaTalonarioPut,db:Session=Depends(get_db)):
    """
    Actualiza la informacion de un talonario en especifico\n
        "valor_boleta"
        "celular":
    """
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()
    talonario.valor_boleta=entrada.valor_boleta
    talonario.celular=entrada.celular
    db.commit()
    db.refresh(talonario)
    return talonario

@routerTalonario.delete(
    '/talonario/{talonario_id}',
    response_model=schemas.Respuesta,
    tags=["Administador-Talonario"])
def eliminar_Talonario(talonario_id:int,db:Session=Depends(get_db)):
    """
    Elimina un talonario en especifico\n
    """
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()
    db.delete(talonario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="El talonario {} fue Eliminado exitosamente".format(talonario_id))
    return respuesta
