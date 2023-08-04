from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from schema.schemas_boleta import SchemaBoleta
from schema.schema_premios import SchemaPremios

class SchemaTalonario(BaseModel):
    id: int
    valor_boleta: int
    celular: str
    cantidad: int
    class Config:
        orm_mode =True

class SchemaPostTalonario(BaseModel):
    valor_boleta: int
    celular: str
    cantidad: int
    premios: List[SchemaPremios]


    class Config:
        orm_mode =True


class SchemaTalonarioXBoleta(BaseModel):
    id: int
    valor_boleta: int
    celular: str
    premios: List[SchemaPremios]
    cantidad: int
    boletas: List[SchemaBoleta]
    class Config:
        orm_mode =True



class TalonarioUpdate(BaseModel):   
    valor_boleta: int
    celular: str
    #fecha_Juego: datetime

    class Config:
        orm_mode =True

   


   