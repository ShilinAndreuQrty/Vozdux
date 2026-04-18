from fastapi import APIRouter, Query
from typing import List, Literal

from app.models import Bond
from app.mock_bonds import MOCK_BONDS

router = APIRouter()


@router.get("/top", response_model=List[Bond])
def get_top(by: Literal["yield", "issuer", "duration"] = Query(default="yield")):
    bonds = list(MOCK_BONDS)

    if by == "yield":
        bonds.sort(key=lambda b: b.yield_percent, reverse=True)
    elif by == "issuer":
        bonds.sort(key=lambda b: b.issuer_rating)
    else:
        bonds.sort(key=lambda b: b.duration)

    return bonds[:5]
