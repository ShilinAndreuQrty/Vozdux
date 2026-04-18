from fastapi import APIRouter
from app.mock_bonds import MOCK_BONDS
from app.models import GoalRequest

router = APIRouter()

# Генерация календаря выплат
def build_payment_schedule(price, coupon, lots):
    """
    Генерирует условный календарь выплат по облигации.
    Частота выплат зависит от купонной ставки.
    """

    if coupon is None:
        return []

    # Определяем частоту выплат
    if coupon < 9:
        periods = 1
        months = ["Декабрь"]
    elif coupon < 12:
        periods = 2
        months = ["Июнь", "Декабрь"]
    else:
        periods = 4
        months = ["Март", "Июнь", "Сентябрь", "Декабрь"]

    invested = price * lots
    annual_income = invested * coupon / 100
    payment = round(annual_income / periods, 2)

    return [{"month": m, "amount": payment} for m in months]

# Эндпоинт /goal
@router.post("/")
def goal(req: GoalRequest):
    amount = req.amount
    target_yield = req.target_yield

    bonds = [bond.model_dump() for bond in MOCK_BONDS]

    # Фильтрация по доходности
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

        bcopy = {
            "ticker": b["ticker"],
            "name": b["name"],
            "price": b["price"],
            "yield_percent": b["yield_percent"],
            "duration": b["duration"],
            "coupon": b.get("coupon"),
            "yield_to_maturity": b.get("yield_to_maturity"),
            "lots": lots,
            "invested": invested,
            "annual_income": annual_income,
        }

        # Добавляем календарь выплат
        bcopy["payment_schedule"] = build_payment_schedule(
            price=b["price"],
            coupon=b.get("coupon"),
            lots=lots
        )

        results.append(bcopy)

    # Сортировка по годовому доходу
    results = sorted(results, key=lambda x: x["annual_income"], reverse=True)

    top5 = results[:5]

    # Средние значения
    avg_yield = sum(b["yield_percent"] for b in top5) / len(top5)
    avg_income = sum(b["annual_income"] for b in top5) / len(top5)

    return {
        "target_yield": target_yield,
        "amount": amount,
        "top_bonds": top5,
        "avg_yield_percent": round(avg_yield, 2),
        "avg_annual_income": round(avg_income, 2)
    }
