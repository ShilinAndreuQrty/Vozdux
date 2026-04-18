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

    yield_percent = arr[:, 0]
    risk = arr[:, 1]
    duration_months = arr[:, 2]
    price = arr[:, 3]

    normalized_yield = yield_percent / 100.0
    risk_penalty = k1 * (risk ** 2)
    duration_penalty = k2 * ((duration_months / 36.0) ** 2)
    discount = (100.0 - price) / 100.0
    risk_distance = np.abs(risk - target_risk) / 3.0
    duration_distance = np.abs(duration_months - target_duration) / max(target_duration, 6.0)

    rating = (
        (normalized_yield * (1 - risk_penalty) * (1 - duration_penalty))
        + (k3 * discount)
        - (k4 * risk_distance)
        - (k5 * duration_distance)
    )
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
        arr.append([yp, r, d, p])

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

def pick_best_and_alternatives(scored_bonds: List[Dict], top_n: int = 3) -> Tuple[Dict, List[Dict], str]:
    """
    Возвращает: best_bond, alternatives (список), explanation (строка)
    """
    if not scored_bonds:
        return None, [], "Нет данных для анализа"

    # Сортируем по rating по убыванию
    sorted_b = sorted(scored_bonds, key=lambda x: x.get("rating", 0.0), reverse=True)

    best = sorted_b[0]
    alternatives = sorted_b[1:top_n]

    # Простое объяснение: почему выбрали лучшую (можно расширить)
    explanation = (
        f"Выбрана облигация {best.get('name','')} ({best.get('ticker','')}) с рейтингом {best.get('rating'):.4f}. "
        f"Доходность {best.get('yield_percent')}%, риск {best.get('risk')}, сроком на {best.get('duration')} мес."
    )

    return best, alternatives, explanation
