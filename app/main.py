# app/main.py
from fastapi import FastAPI
from app.routes import auth, profile, strategy
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(strategy.router, prefix="/api")
