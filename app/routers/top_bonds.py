from fastapi import APIRouter, Query
from app.mock_bonds import MOCK_BONDS
from data.database import calculate_bond_duration
import numpy as np

router = APIRouter()

@router.get("/")
def top_bonds(by: str = Query("yield", enum=["yield", "issuer", "duration"])):
    """
    Возвращает топ-5 облигаций по выбранному параметру:
    - yield    → доходность (по убыванию)
    - issuer   → рейтинг эмитента (по возрастанию)
    - duration → модифицированная дюрация (по возрастанию)
    """

    bonds = [bond.model_dump() for bond in MOCK_BONDS]

    # Доходность 
    if by == "yield":
        sorted_bonds = sorted(bonds, key=lambda x: x["yield_percent"], reverse=True)

    # Рейтинг эмитента 
    elif by == "issuer":
        sorted_bonds = sorted(bonds, key=lambda x: x["issuer_rating"])

    # Дюрация 
    elif by == "duration":
        # создаём numpy-массив всех облигаций
        
        arr = np.array([
        [
            0,
            0,
            b["duration"],       # arr[:,2]
            0,
            b["yield_percent"]   # arr[:,4]
        ]
        for b in bonds
    ])

    durations = calculate_bond_duration(arr)

    for i, bond in enumerate(bonds):
        bond["duration_metric"] = float(durations[i])

    sorted_bonds = sorted(bonds, key=lambda x: x["duration_metric"])


    return {
        "top_list": sorted_bonds[:5],
        "sorted_by": by
    }
