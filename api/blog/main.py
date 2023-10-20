from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from typing import List
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import blog, user, medecin, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(medecin.router)
app.include_router(authentication.router)