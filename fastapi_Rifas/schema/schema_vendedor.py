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
    
class SchemaAsignarBoletas(BaseModel):
    id_talonario : int


class SchemaCantidadBoletasVendedor(BaseModel):
    id_vendedor : int
    cantidad : int
    

class SchemaBoletasAsignadas(BaseModel):
    nombre : str
    rango_inicial : int
    rango_final: int