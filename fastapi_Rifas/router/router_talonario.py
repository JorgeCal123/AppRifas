from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from config.conexion import  get_db

from schema.schema_talonario import SchemaTalonario, SchemaTalonarioPut, SchemaTalonarioXBoleta, SchemaTalonarioPost
from schema.schema_premios import SchemaPremios
from modelo.modelos import Talonario, Premio, id_seis_digitos
import schema.schemas as schemas

from typing import List

from .router_boletas import guardarBoletas, darListaBoletas

from fastapi.responses import JSONResponse

routerTalonario = APIRouter()


@routerTalonario.post('/talonario/', tags=["Talonario"])
def crear_Talonario(entrada:SchemaTalonarioPost, db:Session=Depends(get_db)):
    """
    Crea un talonario con los premios y las boletas de acuerdo a la cantidad que se ingrese\n
    Returns:\n
        "valor_boleta"
        "celular"
        "cantidad"
        "Lista de Premios"
    """
    talonario = Talonario(id = id_seis_digitos(), valor_boleta=entrada.valor_boleta, celular=entrada.celular, cantidad= entrada.cantidad_Boletas)

    # De la lista de schemas de premios recorro cada uno
    for premio in entrada.premios:
        # Saco esa informacion y creo la instacia de premios
        nuevo_premio = Premio(premio = premio.premio, imagen= premio.imagen, fecha_juego=premio.fecha_juego, id_talonario=talonario.id)
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
    guardarBoletas(entrada.cantidad_Boletas, entrada.cantidad_oportunidades, talonario, db)
    data = {"mensaje": "¡Operación exitosa!", "Id_talonario": talonario.id}
    return JSONResponse(content=data, status_code=201)  

@routerTalonario.get('/talonario/',
                     response_model=List[SchemaTalonario],
                     tags=["Talonario"],
                     summary="Mostrar el talanario General")
def mostrar_Talanario_General(db:Session=Depends(get_db)):
    """
    Obtiene una lista de todos los talonarios con su informacion Básica\n\n
    Returns:\n
        id
        valor_boleta
        celular
        cantidad
    """
    talonarios = db.query(Talonario).all()
    
    lista_talonario = []
    for talonario in talonarios:
        datos_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad}
        schema_talonario= SchemaTalonario(**datos_talonario)
        lista_talonario.append(schema_talonario)
    return lista_talonario

@routerTalonario.get('/talonario/{talonario_id}',response_model=SchemaTalonarioXBoleta, tags=["Talonario"])
def mostrar_Talonario_Completo(talonario_id:int,db:Session=Depends(get_db)):
    """
    Obtiene la informacion Completa de un talonario en especifico\n
    Returns:\n
        "id"
        "valor_boleta"
        "celular"
        "cantidad"
        "Lista de Premios"
        "Lista de Boletas"
    """
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()

    lista_boletas= darListaBoletas(talonario)
    premios=[]
    for prem in talonario.premios:
        premio = SchemaPremios(id=prem.id, premio=prem.premio, imagen=prem.imagen, fecha_juego=prem.fecha_juego)
        premios.append(premio)
    schema_premio_talonario= {"id":talonario.id, "valor_boleta":talonario.valor_boleta, "celular":talonario.celular, "cantidad":talonario.cantidad, "boletas": lista_boletas, "premios": premios}
    schema_talonario= SchemaTalonarioXBoleta(**schema_premio_talonario)
    return schema_talonario


@routerTalonario.put('/talonario/{talonario_id}',response_model=SchemaTalonarioPut, tags=["Talonario"])
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

@routerTalonario.delete('/talonario/{talonario_id}',response_model=schemas.Respuesta, tags=["Talonario"])
def eliminar_Talonario(talonario_id:int,db:Session=Depends(get_db)):
    """
    Elimina un talonario en especifico\n
    """
    talonario = db.query(Talonario).filter_by(id=talonario_id).first()
    db.delete(talonario)
    db.commit()
    respuesta = schemas.Respuesta(mensaje="El talonario {} fue Eliminado exitosamente".format(talonario_id))
    return respuesta
