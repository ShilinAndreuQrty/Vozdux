from fastapi import APIRouter, HTTPException
from app.models import Bond
from typing import List

router = APIRouter()

#Мок данные 
MOCK_BONDS = {
    "SU26238RMFS6": Bond(ticker="SU26238RMFS6", name="ООЗ 26238", price=101.2, yield_percent=10.5, risk=1, duration=36),
    "GAZP": Bond(ticker="GAZP", name="Газпром облигация", price=98.7, yield_percent=12.1, risk=2, duration=12),
}


@router.get('/{ticker}', response_model = Bond)
def get_bond(ticker: str):
    bond = MOCK_BONDS.get(ticker.upper())

    if not bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    
    return bond