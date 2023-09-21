from pydantic import BaseModel


class SchemaVendedor(BaseModel):
  mensaje: str


class SchemaVendedorPost(BaseModel):
    cedula: str
    nombre : str
    apellido : str
    celular : str
    correo : str


class SchemaVendedorGet(BaseModel):
    cedula : int
    nombre : str
    apellido : str
    celular : str
    correo : str
    
class SchemaAsignarBoletas(BaseModel):
    id_talonario : int


class SchemaCantidadBoletasVendedor(BaseModel):
    cedula_vendedor : int
    cantidad : int
    

class SchemaBoletasAsignadas(BaseModel):
    cedula_vendedor : int
    nombre : str
    rango_inicial : int
    rango_final: int