from fastapi import APIRouter, Query
from app.mock_bonds import MOCK_BONDS

router = APIRouter()

@router.get("/")
def goal(
    amount: float = Query(..., description="Сумма инвестирования"),
    target_yield: float = Query(..., description="Желаемая доходность в процентах")
):
    bonds = [bond.model_dump() for bond in MOCK_BONDS]

    filtered = [b for b in bonds if float(b["yield_percent"]) >= target_yield]

    if not filtered:
        return {
            "target_yield": target_yield,
            "amount": amount,
            "top_bonds": [],
            "message": "Нет облигаций, удовлетворяющих заданной доходности."
        }

    results = []

    for b in filtered:
        price = float(b["price"])
        lots = int(amount // price)
        invested = round(lots * price, 2)
        annual_income = round(invested * float(b["yield_percent"]) / 100, 2)

        bcopy = b.copy()
        bcopy["lots"] = lots
        bcopy["invested"] = invested
        bcopy["annual_income"] = annual_income

        results.append(bcopy)

    #Сортируем по доходу
    results = sorted(results, key=lambda x: x["annual_income"], reverse=True)

    top5 = results[:5]

    # Метрики для графиков 
    avg_yield = sum(b["yield_percent"] for b in top5) / len(top5)
    avg_income = sum(b["annual_income"] for b in top5) / len(top5)

    return {
        "target_yield": target_yield,
        "amount": amount,
        "top_bonds": top5,
        "avg_yield_percent": round(avg_yield, 2),
        "avg_annual_income": round(avg_income, 2)
    }
