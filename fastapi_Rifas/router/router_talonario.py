from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from config.conexion import  get_db

from schema.schema_talonario import SchemaTalonario, SchemaTalonarioPut, SchemaTalonarioXBoleta, SchemaTalonarioPost
from schema.schema_premios import SchemaPremios
from modelo.modelos import Talonario, Premio, id_seis_digitos
import schema.schemas as schemas

from app.appBoletas import crearBoletas
from typing import List

from .router_boletas import guardarBoletas, darListaBoletas

routerTalonario = APIRouter()

@routerTalonario.get('/talonario/',response_model=List[SchemaTalonario])
def mostrar_Talanario(db:Session=Depends(get_db)):
    talonarios = db.query(Talonario).all()
    
    lista_talonario = []
    for talonario in talonarios:
        datos_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad}
        schema_talonario= SchemaTalonario(**datos_talonario)
        lista_talonario.append(schema_talonario)
    return lista_talonario

@routerTalonario.get('/talonario/{talonario_id}',response_model=SchemaTalonarioXBoleta)
def mostrar_boletas_talonario(talonario_id:int,db:Session=Depends(get_db)):
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()

    lista_boletas= darListaBoletas(talonario)
    premios=[]
    for prem in talonario.premios:
        premio = SchemaPremios(id=prem.id, premio=prem.premio,imagen=prem.imagen, fecha_Juego=prem.fecha_Juego)
        premios.append(premio)
    schema_premio_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad, "boletas": lista_boletas, "premios": premios}
    schema_talonario= SchemaTalonarioXBoleta(**schema_premio_talonario)
    return schema_talonario

"""
  SchemaTalonarioPost
    valor_boleta: 
    celular: 
    cantidad: 
    premios: List[SchemaPremios]


"""
@routerTalonario.post('/talonario/',response_model=SchemaTalonarioPost)
def crear_Talonario(entrada:SchemaTalonarioPost, db:Session=Depends(get_db)):
    # Crea una instancia de Talonario
    talonario = Talonario(id = id_seis_digitos(), valor_boleta=entrada.valor_boleta, celular=entrada.celular, cantidad= entrada.cantidad)

    # De la lista de schemas de premios recorro cada uno
    for premio in entrada.premios:
        # Saco esa informacion y creo la instacia de premios
        nuevo_premio = Premio(premio = premio.premio, imagen= premio.imagen, fecha_juego=premio.fecha_Juego, id_talonario=talonario.id)
        talonario.premios.append(nuevo_premio)
    """
        Llamo metodo crearBoletas que me entrega un diccionario que contiene una lista de numeros
        y el código qr
    """
    """
    llamo el metodo guardar boleta que me recibe por parametro:
        numeros_boleta: el metodo de arriba
        talonria: La instancia del talonario (linea 55)
        db: la sesion en la que estamos actualmente en la base de datos
    """
    guardarBoletas(crearBoletas(entrada.cantidad), talonario, db)
    return entrada


@routerTalonario.put('/talonario/{talonario_id}',response_model=SchemaTalonarioPut)
def actualizar_Talonario(talonario_id:int,entrada:SchemaTalonarioPut,db:Session=Depends(get_db)):
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()
    talonario.valor_boleta=entrada.valor_boleta
    talonario.celular=entrada.celular
    talonario.fecha_Juego=entrada.fecha_Juego
    db.commit()
    db.refresh(talonario)
    return talonario

@routerTalonario.delete('/talonario/{talonario_id}',response_model=schemas.Respuesta)
def eliminar_Talonario(boleta_id:int,db:Session=Depends(get_db)):
    boleta = db.query(Talonario).filter_by(id=boleta_id).first()
    db.delete(boleta)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
    return respuesta
