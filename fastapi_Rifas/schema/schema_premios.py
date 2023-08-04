from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class SchemaPremios(BaseModel):
    id: int
    premio: str
    imagen: str
    fecha_Juego: datetime
    #fecha_Juego: datetime
    class Config:
        orm_mode =True

class Schema_info_Juegos(BaseModel):
    dia: str
    premio: List[str]
    fecha: datetime
    ganador: Optional[List[int]]


class Schema_ganador(BaseModel):
    fecha: datetime
    premio: str
    boleta_ganadora: int

class Schema_basic_ganadores(BaseModel):
    ganadores: List[Schema_ganador]

