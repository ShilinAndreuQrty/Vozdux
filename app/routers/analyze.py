# app/routers/analyze.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.logic import score_bonds, pick_best_and_alternatives
from app.models import UserInput

router = APIRouter()

# Пример мок-списка облигаций (можно заменить на реальный источник)
MOCK_BONDS = [
    {"ticker": "SU26238RMFS6", "name": "ОФЗ 26238", "price": 101.2, "yield_percent": 10.5, "risk": 1, "duration": 36},
    {"ticker": "GAZP", "name": "Газпром облигация", "price": 98.7, "yield_percent": 12.1, "risk": 2, "duration": 12},
    {"ticker": "SU26240RMFS", "name": "ОФЗ 26240", "price": 98.5, "yield_percent": 11.8, "risk": 1, "duration": 24},
]

@router.post('/')
def analyze(user_input: UserInput):
    """
    Приходит от фронта: amount, risk, duration.
    Берём список облигаций (здесь мок), считаем рейтинг, возвращаем best_bond, alternatives, explanation.
    """
    # TODO: при интеграции заменить MOCK_BONDS на реальный источник (база/файл/сервис)
    bonds = MOCK_BONDS.copy()

    filtered = [b for b in bonds if b.get("risk", 0) <= user_input.risk]

    # Считаем рейтинги
    scored = score_bonds(filtered)

    # Берём лучшую и альтернативы
    best, alternatives, explanation = pick_best_and_alternatives(scored, top_n=3)

    # Формат ответа, который ждёт фронт
    return {
        "best_bond": best,
        "alternatives": alternatives,
        "explanation": explanation
    }
