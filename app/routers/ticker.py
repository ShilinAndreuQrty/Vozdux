from fastapi import APIRouter, HTTPException
from app.models import Bond
from app.mock_bonds import MOCK_BONDS_BY_TICKER

router = APIRouter()

@router.get('/{ticker}', response_model = Bond)
def get_bond(ticker: str):
    bond = MOCK_BONDS_BY_TICKER.get(ticker.upper())

    if not bond:
        raise HTTPException(status_code=404, detail="Bond not found")
    
    return bond