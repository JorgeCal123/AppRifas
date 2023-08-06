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
"""
{
  dia: lunes // Premio
  premio: [20000, 10000, 50000] // Premio
  fecha: 2023/08/18 // Premio
  ganador: [2304, 2556, 1245] //Ganador
} 
"""

class SchemaGanador(BaseModel):
    fecha: datetime
    premio: str
    boleta_ganadora: int

class SchemaBasicGanadores(BaseModel):
    ganadores: List[SchemaGanador]

