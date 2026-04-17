from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

@router.get('/test')
def test():
    return {"status": "ok"}