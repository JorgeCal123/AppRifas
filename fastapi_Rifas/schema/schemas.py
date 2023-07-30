from pydantic import BaseModel

class Respuesta(BaseModel):   
    mensaje:str
    code:int
    nommbre: str
   


   