from fastapi import FastAPI
from config.conexion import engine
from router.router_boletas import routerBoletas
from router.router_talonario import routerTalonario
from router.router_ganadores import routerGanadoras
from router.router_premios import routerPremios
from router.router_cliente import routerCliente
from router.router_vendedor import routerVendedor
from router.router_administrador import routerAdmin

import uvicorn
import modelo.modelos as models
import datetime
from app.fechas_semana import obtener_fechas_lunes_a_domingo
from fastapi.openapi.models import Info

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    description="""
    Descripcion para el uso de la api de Rifas \n
        Pagina de inicio \n
    Apis
    Apis2
    
    """
)

app.include_router(routerAdmin)
app.include_router(routerTalonario)
app.include_router(routerVendedor)

#app.include_router(routerBoletas)
app.include_router(routerGanadoras)
app.include_router(routerPremios)
app.include_router(routerCliente)


if __name__== "__main__":
    print(obtener_fechas_lunes_a_domingo())
    uvicorn.run("main:app", port=8000, reload=True)
