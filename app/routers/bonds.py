from app.models import Bond
from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get('/list', response_model=List[Bond])
def get_bonds():
    #мок данные 
    return [
        Bond(ticker="SU26238RMFS6", name="ООЗ 26238", price=101.2, yield_percent=10.5, risk=1, duration = 36),
        Bond(ticker="GAZP", name="Газпром облигация", price=98.7, yield_percent=12.1, risk=2, duration = 12),
    ]