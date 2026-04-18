from fastapi import FastAPI

from app.routers.bonds import router as bonds_router
from app.routers.analyze import router as analyze_router
from app.routers.ticker import router as ticker_router
from app.routers.health import router as health_router 
from app.routers.top_bonds import router as top_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(bonds_router, prefix='/bonds')
app.include_router(analyze_router, prefix='/analyze')
app.include_router(ticker_router, prefix='/bonds')
app.include_router(health_router, prefix = '/health')
app.include_router(top_router, prefix='/top')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)