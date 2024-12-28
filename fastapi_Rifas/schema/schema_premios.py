from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator


"""
    Esquema para mostrar los premios de un talonario.

    Atributos:
        premio (str): 
            El nombre o descripción del premio que se rifará.
        imagen (str): 
            URL o dirección de la imagen que representa el premio.
        fecha_juego (datetime): 
            Fecha del día que se hace el sorteo para este premio.
"""
class SchemaPremios(BaseModel):
    premio: str
    imagen: str
    fecha_juego: datetime

    @validator('fecha_juego', pre=True, always=True)
    def validar_fecha(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d/%m/%Y")
            except ValueError:
                raise ValueError("El formato de la fecha debe ser dd/mm/yyyy")
        return v
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



