from fastapi import FastAPI
from config.conexion import engine
from router.router_boletas import routerBoletas
from router.router_talonario import routerTalonario
from router.router_ganadores import routerGanadoras
from router.router_premios import routerPremios
from router.router_cliente import routerCliente
import uvicorn
import model.models as models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(routerTalonario)

app.include_router(routerBoletas)
app.include_router(routerGanadoras)
app.include_router(routerPremios)
app.include_router(routerCliente)
if __name__== "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
