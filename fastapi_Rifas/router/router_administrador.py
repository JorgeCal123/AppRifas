from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from config.conexion import  get_db
from schema.schema_talonario import *
from modelo.modelos import *



routerAdmin= APIRouter()


@routerAdmin.get('/admin/opcionestalonario',response_model=list[SchemaTalonarioXpremio])
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