from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from schema.schema_boleta import SchemaBoleta
from schema.schema_premios import SchemaPremios


class SchemaTalonario(BaseModel):
    id: int
    valor_boleta: int
    celular: str
    cantidad: int
    class Config:
        orm_mode =True

class SchemaTalonarioPost(BaseModel):
    valor_boleta: int
    celular: str
    cantidad_Boletas: int
    cantidad_oportunidades: int
    premios: List[SchemaPremios]

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
   
class SchemaTalonarioXpremio(BaseModel):   
    id_talonario: int
    premios: List[SchemaInfopremio]
    
class SchemaInfoVendedor(BaseModel):
  id : int
  nombre : str

    
class SchemaTalonarioXvendedor(BaseModel):
    id_talonario: int
    cantidad : int
    vendedores : List[SchemaInfoVendedor]

