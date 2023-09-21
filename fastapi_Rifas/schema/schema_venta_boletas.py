from pydantic import BaseModel


class SchemaVenta(BaseModel):
  consecutiva_id: int
  pagada: bool


class Schema_Boleta_vendida(BaseModel):
  id: int
