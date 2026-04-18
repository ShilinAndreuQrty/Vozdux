from fastapi import APIRouter, Query
from app.mock_bonds import MOCK_BONDS
from data.database import calculate_bond_duration
import numpy as np

router = APIRouter()

@router.get("/")
def top_bonds(by: str = Query("yield", enum=["yield", "duration", "ytm", "coupon"])):
    """
    Возвращает топ-5 облигаций по выбранному параметру.

    Параметры сортировки:
    - yield    → сортировка по текущей доходности (по убыванию)
    - duration → сортировка по модифицированной дюрации (по возрастанию)
    - ytm      → сортировка по доходности к погашению (по убыванию)
    - coupon   → сортировка по купонной ставке (по убыванию)

    Каждая облигация в ответе содержит:
    - ticker
    - name
    - price
    - yield_percent
    - duration
    - coupon
    - yield_to_maturity
    """

    # Преобразуем модели в dict
    bonds = [bond.model_dump() for bond in MOCK_BONDS]

    # Сортировка по текущей доходности
    if by == "yield":
        sorted_bonds = sorted(
            bonds,
            key=lambda x: x["yield_percent"],
            reverse=True
        )

    # Сортировка по модифицированной дюрации 
    elif by == "duration":
        arr = np.array([
            [
                0,
                0,
                b["duration"],
                0,
                b["yield_percent"]
            ]
            for b in bonds
        ])

        durations = calculate_bond_duration(arr)

        for i, bond in enumerate(bonds):
            bond["duration_metric"] = float(durations[i])

        sorted_bonds = sorted(
            bonds,
            key=lambda x: x["duration_metric"]
        )

    # Сортировка по доходности к погашению (YTM) 
    elif by == "ytm":
        sorted_bonds = sorted(
            bonds,
            key=lambda x: x.get("yield_to_maturity", 0),
            reverse=True
        )

    #  Сортировка по купону 
    elif by == "coupon":
        sorted_bonds = sorted(
            bonds,
            key=lambda x: x.get("coupon", 0),
            reverse=True
        )

    # Формируем финальный список 
    top5 = []
    for b in sorted_bonds[:5]:
        top5.append({
            "ticker": b["ticker"],
            "name": b["name"],
            "price": b["price"],
            "yield_percent": b["yield_percent"],
            "duration": b["duration"],
            "coupon": b.get("coupon"),
            "yield_to_maturity": b.get("yield_to_maturity")
        })

    return {
        "top_list": top5,
        "sorted_by": by
    }
