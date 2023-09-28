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
    
class SchemaVentasVendedor(BaseModel):

  nombre_vendedor: str
  cantidad_boletas_asignadas: int
  cantidad_boletas_vendidas: int
  precio_unitario: int
  total_ventas: int
  pago: int
  rango_asignado: str
  
class SchemaTalonarioVentasVendedor(BaseModel):
    
  premio: str
  talonario_id : int
  ventas_vendedor: list[SchemaVentasVendedor]