from pydantic import BaseModel
from typing import Optional, List


class SchemaVenta(BaseModel):
  consecutiva_id: int
  pagada: bool


class Schema_Boleta_vendida(BaseModel):
  id: int

class SchemaClienteBoletas(BaseModel):
    
    nombre : Optional[str]
    apellido : Optional[str]
    celular : str
    direccion : Optional[str]
    notificacion : bool
    venta_boletas: List[SchemaVenta]