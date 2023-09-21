from pydantic import BaseModel
from typing import Optional, List

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