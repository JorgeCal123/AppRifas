from pydantic import BaseModel


class SchemaVendedor(BaseModel):
  mensaje: str


class SchemaVendedorPost(BaseModel):
   
    nombre : str
    apellido : str
    celular : str
    correo : str


class SchemaVendedorGet(BaseModel):
    id : int
    nombre : str
    apellido : str
    celular : str
    correo : str
