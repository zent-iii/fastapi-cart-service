from fastapi import FastAPI
from schemas.schema import ShopName
from routers.routes import routers as routes_router

from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routes_router, tags=["Webshop Routes"])

@app.get('/', tags=["Root"])
def route():
    return {f'Welcome in {ShopName}'}