from fastapi import APIRouter
from app.logic import score_bonds, pick_best_and_alternatives
from app.models import UserInput, AnalyzeResponse
from app.mock_bonds import MOCK_BONDS

router = APIRouter()

@router.post('/', response_model=AnalyzeResponse)
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
        yield_percent = float(best.get("yield_percent", 0))
        
        if user_input.mode == "by_sum":
            # Режим: от суммы вложений
            estimated_lots = int(user_input.amount // lot_price) if lot_price > 0 else 0
            invested_amount = round(estimated_lots * lot_price, 2)
            estimated_annual_income = round(
                invested_amount * yield_percent / 100.0,
                2
            )
            projection = {
                "estimated_lots": estimated_lots,
                "invested_amount": invested_amount,
                "estimated_annual_income": estimated_annual_income,
                "required_capital": None
            }
        else:
            # Режим: от желаемого дохода (по месяцам)
            # user_input.amount = целевой доход в месяц
            # Формула: required_capital = (target_income_per_month * 12) / (yield_percent / 100)
            target_annual_income = user_input.amount * 12
            
            if yield_percent > 0:
                required_capital = round(target_annual_income / (yield_percent / 100.0), 2)
                lot_price_for_capital = float(best.get("price", 0))
                estimated_lots = int(required_capital // lot_price_for_capital) if lot_price_for_capital > 0 else 0
            else:
                required_capital = 0
                estimated_lots = 0
            
            projection = {
                "estimated_lots": estimated_lots,
                "invested_amount": required_capital,
                "estimated_annual_income": target_annual_income,
                "required_capital": required_capital
            }

    return {
        "best_bond": best,
        "alternatives": alternatives,
        "explanation": explanation,
        "projection": projection,
        "required_capital": projection.get("required_capital") if projection else None
    }
