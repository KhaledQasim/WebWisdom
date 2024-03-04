from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from .database import models
from .database.database import SessionLocal, engine

from .routers import auth
from .app import api
from .config.config import Config


app = FastAPI()
app.include_router(auth.router)
app.include_router(api.router)


# Below is to allow CORS for our frontend to access our backend API.

# ------------------------------------------------------------
origins = [
    "http://localhost",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://127.0.0.2:5174",
    Config.ALLOWED_FRONTEND_URL


]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type',
                   'Authorization', 'Access-Control-Allow-Origin'],
)
# ------------------------------------------------------------


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main_get():
    return JSONResponse(content="omar")
