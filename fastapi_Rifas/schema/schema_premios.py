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

class SchemaInfoJuegos(BaseModel):
    dia: str
    premio: List[str]
    fecha: datetime
    ganador: Optional[List[int]]


class SchemaGanador(BaseModel):
    fecha: datetime
    premio: str
    boleta_ganadora: int

class SchemaBasicGanadores(BaseModel):
    ganadores: List[SchemaGanador]

