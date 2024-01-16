from fastapi import FastAPI
from . import models
from .database import engine
from .routers import medecin, authentication, rapport, visiteur

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(visiteur.router)
app.include_router(medecin.router)
app.include_router(rapport.router)
app.include_router(authentication.router)
