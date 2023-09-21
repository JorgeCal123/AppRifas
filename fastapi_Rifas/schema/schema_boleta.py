from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from schema.schema_numero_boletas import SchemaNumeroBoleta

class SchemaBoleta(BaseModel):
    id: Optional[int]
    id_talonario:Optional[int]
    consecutiva_id: Optional[int]
    qr_code: str
    estado_venta: Optional[bool]
    estado_pagado: Optional[bool]
    numeros: List[int]
    # Sirve para dar soporte al mapeo de los objetos del orm
    class Config:
        orm_mode =True

class SchemaTolonarioBoleta(BaseModel):
    id: Optional[int]
    # Sirve para dar soporte al mapeo de los objetos del orm
    class Config:
        orm_mode =True


"""class postBoleta(PostBase):
    id: Optional[int]
    id_vendedor: Optional[int]
    id_cliente: Optional[int]
    qr_code: str
    detalle: str
    pagado: bool
    fecha_venta: datetime
"""

class BoletaActualizar(BaseModel): 
    id_vendedor: Optional[int]
    id_cliente: Optional[int]
    qr_code: str
    detalle: str
    pagado: bool
    fecha_venta: datetime
    class Config:
        orm_mode =True
   