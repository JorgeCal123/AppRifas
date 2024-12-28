from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from schema.schema_boleta import SchemaBoleta
from schema.schema_premios import SchemaPremios

"""
    Esquema para la creación de un talonario.

    Atributos:
        valor_boleta (int): 
            Representa el precio de cada boleta en el talonario.
        celular (str): 
            Número de contacto de la sede o responsable de la rifa. Debe ser una cadena de hasta 10 caracteres.
        cantidad_Boletas (int): 
            Cantidad total de boletas que contiene el talonario.
        cantidad_oportunidades (int): 
            Cantidad de oportunidades es la cantidad de numeros que ofrece la boleta se puede crear solo 2, 3, 8 o 10 numeros
        premios (List[SchemaPremios]): 
            Lista de premios asociados al talonario
"""
class SchemaTalonarioPost(BaseModel):
    valor_boleta: int
    celular: str
    cantidad_Boletas: int
    cantidad_oportunidades: int
    premios: List[SchemaPremios]

    class Config:
        orm_mode =True


class SchemaTalonario(BaseModel):
    id: int
    valor_boleta: int
    celular: str
    cantidad: int
    infopremio: List["SchemaInfopremio"]

    class Config:
        orm_mode =True



class SchemaTalonarioXBoleta(BaseModel):
    id: int
    valor_boleta: int
    celular: str
    cantidad: int
    premios: List[SchemaPremios]
    boletas: List[SchemaBoleta]
    class Config:
        orm_mode =True



class SchemaTalonarioPut(BaseModel):   
    valor_boleta: int
    celular: str
    class Config:
        orm_mode =True

class SchemaInfopremio(BaseModel):
    premio: str
    fecha: str
    class Config:
        orm_mode =True
    
class SchemaTalonarioXpremio(BaseModel):   
    id_talonario: int
    premios: List[SchemaInfopremio]
    
class SchemaInfoVendedor(BaseModel):
  id : int
  nombre : str

class SchemaVendedorXBoleta(BaseModel):
  id : int
  nombre : str
  boletas: str

class SchemaTalonarioXvendedor(BaseModel):
    id_talonario: int
    cantidad : int
    vendedores : List[SchemaVendedorXBoleta]

