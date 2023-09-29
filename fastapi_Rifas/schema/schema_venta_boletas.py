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

  nombre_vendedor: Optional[str] = None
  cantidad_boletas_asignadas: Optional[int] = None
  cantidad_boletas_vendidas: Optional[int] = None
  precio_unitario: Optional[int] = None
  total_ventas: Optional[int] = None
  pago: Optional[int] = None
  rango_asignado: Optional[str] = None
  
class SchemaTalonarioVentasVendedor(BaseModel):
    
  talonario_id : int
  fecha_juego: str
  ventas_vendedor: Optional[List[SchemaVentasVendedor]]