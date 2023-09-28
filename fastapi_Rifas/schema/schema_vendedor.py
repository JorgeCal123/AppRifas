from pydantic import BaseModel
from typing import Optional

class SchemaVendedor(BaseModel):
  mensaje: str


class SchemaVendedorPost(BaseModel):
    cedula: str
    nombre : str
    apellido : str
    celular : str
    correo : str


class SchemaVendedorGet(BaseModel):
    cedula : str
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
    
class SchemaVendedorPut(BaseModel):
    cedula: Optional[str] = None
    nombre : Optional[str] = None
    apellido : Optional[str] = None
    celular : Optional[str] = None
    correo : Optional[str] = None

class SchemaPorcentajeVendedor(BaseModel):
    valor_boleta : int
    porcentaje : int
