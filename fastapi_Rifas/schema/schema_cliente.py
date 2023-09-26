from pydantic import BaseModel
from typing import Optional, List
from schema.schema_venta_boletas import Schema_Boleta_vendida

class SchemaCliente(BaseModel):
  mensaje: str
  
class SchemaBoleta(BaseModel):
   fecha: str
   conscutive_id: str
   oportunidades: List[str]
   nombre_vendedor: str
   estado_pago: bool

class SchemaClienteGet(BaseModel):

    id : int
    nombre : str
    apellido : str
    celular : str
    direccion : str
    notificacion : bool
    boletas: List[SchemaBoleta]

class SchemaClienteBasic(BaseModel):

    id : int
    nombre : str
    apellido : str
    celular : str
    direccion : str
    notificacion : bool

class SchemaClientePost(BaseModel):
    
    nombre : Optional[str]
    apellido : Optional[str]
    celular : str
    direccion : Optional[str]
    notificacion : bool


class SchemaClientePatch(BaseModel):
    
    nombre : Optional[str] = None
    apellido : Optional[str] = None
    celular : Optional[str] = None
    direccion : Optional[str] = None
    notificacion : Optional[bool] = None

    

class SchemaBoletaDetalle(BaseModel):
  id: int
  fecha_venta : str
  consecutiva_id : int
  numeros : List[int]
  vendedor : str
  estado_pagado : bool
  fecha_juego : str
  
    
class SchemaClienteDetalles(BaseModel):
    nombre : str
    notificacion : bool
    info_boleta :  List[SchemaBoletaDetalle]
   
    
    
