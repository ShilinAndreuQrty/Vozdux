# app/routers/analyze.py
from fastapi import APIRouter
from app.logic import score_bonds, pick_best_and_alternatives
from app.models import UserInput, AnalyzeResponse
from app.mock_bonds import MOCK_BONDS

router = APIRouter()

<<<<<<< Updated upstream
@router.post('/', response_model=AnalyzeResponse)
=======
# Пример мок-списка облигаций (можно заменить на реальный источник)
MOCK_BONDS = [
    {"ticker": "SU26238RMFS6", "name": "ОФЗ 26238", "price": 101.2, "yield_percent": 10.5, "risk": 1, "duration": 36, "issuer_rating": "AAA(RU)"},
    {"ticker": "GAZP", "name": "Газпром облигация", "price": 98.7, "yield_percent": 12.1, "risk": 2, "duration": 12, "issuer_rating": "AA+(RU)"},
    {"ticker": "SU26240RMFS", "name": "ОФЗ 26240", "price": 98.5, "yield_percent": 11.8, "risk": 1, "duration": 24, "issuer_rating": "AAA(RU)"},
]

@router.post('/')
>>>>>>> Stashed changes
def analyze(user_input: UserInput):
    """
    Приходит от фронта: amount, risk, duration.
    Берём список облигаций (здесь мок), считаем рейтинг, возвращаем best_bond, alternatives, explanation.
    """
    bonds = [bond.model_dump() for bond in MOCK_BONDS]
    filtered_by_risk = [b for b in bonds if b.get("risk", 0) <= user_input.risk]
    duration_window = 12
    filtered = [
        b for b in filtered_by_risk
        if abs(float(b.get("duration", 0)) - float(user_input.duration)) <= duration_window
    ]
    if not filtered:
        filtered = filtered_by_risk

    # Считаем рейтинги
    scored = score_bonds(
        filtered,
        target_risk=user_input.risk,
        target_duration=user_input.duration
    )

    # Берём лучшую и альтернативы
    best, alternatives, explanation = pick_best_and_alternatives(scored, top_n=3)

    projection = None
    if best:
        lot_size = 1
        lot_price = float(best.get("price", 0)) * lot_size
        estimated_lots = int(user_input.amount // lot_price) if lot_price > 0 else 0
        invested_amount = round(estimated_lots * lot_price, 2)
        estimated_annual_income = round(
            invested_amount * float(best.get("yield_percent", 0)) / 100.0,
            2
        )
        projection = {
            "estimated_lots": estimated_lots,
            "invested_amount": invested_amount,
            "estimated_annual_income": estimated_annual_income
        }

    return {
        "best_bond": best,
        "alternatives": alternatives,
        "explanation": explanation,
        "projection": projection
    }
