from fastapi import FastAPI
from config.Conexion import engine
from router.router_boletas import routerBoletas
from router.router_talonario import routerTalonario
import uvicorn
import model.models as models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(routerTalonario)

app.include_router(routerBoletas)

if __name__== "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
