from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class SchemaPremios(BaseModel):
    premio: str
    imagen: str
    fecha_juego: datetime
    #fecha_Juego: datetime
    class Config:
        orm_mode =True

  
class SchemaInfoGanador(BaseModel):
    premio: str
    ganador: Optional[int]
    

class SchemaInfoJuegos(BaseModel):
    dia: str
    fecha: str
    premios: List[SchemaInfoGanador]
"""
{
  dia: lunes // Premio
  premio: [20000, 10000, 50000] // Premio
  fecha: 2023/08/18 // Premio
  ganador: [2304, 2556, 1245] //Ganador
} 
"""

class SchemaJuegosPasados(BaseModel):
    fecha: str
    premio: str
    boleta_ganadora: int



