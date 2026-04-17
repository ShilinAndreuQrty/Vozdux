from fastapi import FastAPI
from pydantic import BaseModel

from app.routers.test import router as test_router
from app.routers.bonds import router as bonds_router
from app.routers.analyze import router as analyze_router

from fastapi.middleware.cors import CORSMiddleware


import requests

app = FastAPI()

app.include_router(test_router, prefix='/test')
app.include_router(bonds_router, prefix='/bonds')
app.include_router(analyze_router, prefix='/analyze')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)