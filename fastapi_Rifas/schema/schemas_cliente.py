from pydantic import BaseModel

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
   
    nombre : str
    apellido : str
    celular : str
    direccion : str
    notificacion : bool