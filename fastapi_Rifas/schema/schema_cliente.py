from pydantic import BaseModel
from typing import Optional, List
from schema.schema_venta_boletas import Schema_Boleta_vendida

class SchemaCliente(BaseModel):
  mensaje: str
  
class SchemaClienteGet(BaseModel):

    id : int
    nombre : str
    apellido : str
    celular : str
    direccion : str
    notificacion : bool
  
class SchemaClientePost(BaseModel):
    
    nombre : Optional[str]
    apellido : Optional[str]
    celular : str
    direccion : Optional[str]
    notificacion : bool
    
class SchemaClienteBoletas(BaseModel):
    
    nombre : Optional[str]
    apellido : Optional[str]
    celular : str
    direccion : Optional[str]
    notificacion : bool
    id_boletas: List[Schema_Boleta_vendida]