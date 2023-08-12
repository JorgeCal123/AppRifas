from pydantic import BaseModel
from typing import Optional

"""
  Schema que se retorna al registrar un numero ganador
"""


class SchemaGanador(BaseModel):

  id_boleta: int
  nombre: Optional[str]
  celular: Optional[str]
  numero_ganador: int
  estado_venta: bool
  estado_pagado: bool
  estado_premio: str
  

"""
  schema que registra un nùmero ganador
"""

class SchemaGanadorPost(BaseModel):
  numero_ganador: int