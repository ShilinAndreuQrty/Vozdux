from app.models import Bond
from fastapi import APIRouter
from typing import List
from app.mock_bonds import MOCK_BONDS

router = APIRouter()

@router.get('/list', response_model=List[Bond])
def get_bonds():
    return MOCK_BONDS