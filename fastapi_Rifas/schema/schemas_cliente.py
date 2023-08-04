from pydantic import BaseModel

class SchemaCliente(BaseModel):
  mensaje: str
  
class SchemaClientePost(BaseModel):
   
    nombre : str
    apellido : str
    celular : str
    direccion : str
    notificacion : bool