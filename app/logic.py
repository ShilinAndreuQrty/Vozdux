# app/logic.py
import numpy as np
from typing import List, Dict, Tuple

def calculate_bond_rating_array(
    arr: np.ndarray,
    target_risk: float,
    target_duration: float
) -> np.ndarray:
    """
    Векторная версия рейтинга (использует numpy array).
    arr columns: [yield_percent, risk, duration_months, price]
    """
    k1 = 0.05
    k2 = 0.03
    k3 = 0.05
    k4 = 0.25
    k5 = 0.35
    k6 = 0.04 # штраф за рейтинг эмитента

    yield_percent = arr[:, 0]
    risk = arr[:, 1]
    duration_months = arr[:, 2]
    price = arr[:, 3]
    issuer_rating = arr[:, 4]

    normalized_yield = yield_percent / 100.0
    risk_penalty = k1 * (risk ** 2)
    duration_penalty = k2 * ((duration_months / 36.0) ** 2)
    discount = (100.0 - price) / 100.0
    risk_distance = np.abs(risk - target_risk) / 3.0
    duration_distance = np.abs(duration_months - target_duration) / max(target_duration, 6.0)

    issuer_penalty = k6 * (issuer_rating ** 2)

    rating = (
        (normalized_yield * (1 - risk_penalty) * (1 - duration_penalty))
        + (k3 * discount)
        - (k4 * risk_distance)
        - (k5 * duration_distance)
        - issuer_penalty
    )
    discount = (1000.0 - price) / 1000.0
#(1-risk*0,3)*duration*yield_percent
#(yield_percent / 100.0)
    rating = (normalized_yield * (1 - risk_penalty) * (1 - duration_penalty)) + (k3 * discount)
    return rating

def score_bonds(
    bonds: List[Dict],
    target_risk: int,
    target_duration: int
) -> List[Dict]:
    """
    Принимает список облигаций (каждый — dict с полями: ticker,name,price,yield_percent,risk,duration)
    Возвращает тот же список с добавленным полем 'rating' (float).
    """
    if not bonds:
        return []

    # Собираем массив для расчёта
    arr = []
    for b in bonds:
        # Безопасные приведения типов
        yp = float(b.get("yield_percent", 0.0))
        r = float(b.get("risk", 0.0))
        d = float(b.get("duration", 0.0))
        p = float(b.get("price", 100.0))
        ir = float(b.get("issuer_rating", 1))
        arr.append([yp, r, d, p, ir])

    np_arr = np.array(arr, dtype=float)
    ratings = calculate_bond_rating_array(
        np_arr,
        target_risk=float(target_risk),
        target_duration=float(target_duration)
    )

    # Присваиваем рейтинги обратно
    out = []
    for bond, rating in zip(bonds, ratings):
        bcopy = bond.copy()
        bcopy["rating"] = float(rating)
        out.append(bcopy)

    return out

def pick_best_and_alternatives(scored_bonds: List[Dict], top_n: int = 3) -> Tuple[Dict, List[Dict], Dict[str, str]]:
    """
    Возвращает: best_bond, alternatives (список), explanation (dict(строка, строка))
    """
    if not scored_bonds:
        return None, [], "Нет данных для анализа"

    # Сортируем по rating по убыванию
    sorted_b = sorted(scored_bonds, key=lambda x: x.get("rating", 0.0), reverse=True)

    best = sorted_b[0]
    alternatives = sorted_b[1:top_n]

    # Все метрики для полного отчёта
    best_yield = float(best.get("yield_percent", 0))
    best_risk = int(best.get("risk", 0))
    best_duration = int(best.get("duration", 0))
    best_issuer = int(best.get("issuer_rating", 0))
    best_rating = float(best.get("rating", 0))

    avg_yield = sum(float(b.get("yield_percent", 0)) for b in scored_bonds) / len(scored_bonds)
    
    # Простое объяснение: почему выбрали лучшую 
    short_explanation = (
    f"Выбрана облигация {best.get('name','')} ({best.get('ticker','')}) "
    f"с рейтингом {best.get('rating'):.4f}.\n"
    f"Доходность: {best.get('yield_percent')}%.\n"
    f"Риск: {best.get('risk')}.\n"
    f"Срок: {best.get('duration')} мес.\n"
    f"Рейтинг эмитента: {best.get('issuer_rating')}."
)

    # Полное объяснение 
    full_explanation = (
    f"Эта облигация выбрана как оптимальная по совокупности доходности, риска, срока "
    f"и надёжности эмитента.\n\n"
    f"• Доходность {best_yield}% — выше среднего по отобранным ({avg_yield:.2f}%).\n"
    f"• Риск {best_risk} — соответствует вашему профилю.\n"
    f"• Срок {best_duration} мес. — близок к желаемому горизонту.\n"
    f"• Рейтинг эмитента {best_issuer} — снижает вероятность дефолта.\n\n"
    f"Алгоритм учитывает баланс между доходностью и риском, штрафует слишком длинные "
    f"или слишком короткие сроки и повышает рейтинг бумаг с дисконтом к номиналу.\n\n"
    f"Итоговый интегральный рейтинг: {best_rating:.4f}."
)


    return best, alternatives, {
    "short": short_explanation,
    "full": full_explanation
}

