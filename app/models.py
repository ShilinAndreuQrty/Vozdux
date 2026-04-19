from pydantic import BaseModel
from typing import List, Optional

#Облигация
class Bond(BaseModel):
    ticker: str
    name: str
    price: float
    yield_percent: float
    risk: int
    duration: int
    issuer_rating: int
    coupon: Optional[float] = None
    yield_to_maturity: Optional[float] = None


#Ввод пользователя 
class UserInput(BaseModel):
    amount : float
    risk : int 
    duration : int
    mode: str = "by_sum"  # "by_sum" или "by_target" 


class Projection(BaseModel):
    estimated_lots: int
    invested_amount: float
    estimated_annual_income: float
    required_capital: Optional[float] = None  # Для режима by_target


class Explanation(BaseModel):
    short: str
    full: str

class AnalyzeResponse(BaseModel):
    best_bond: Bond
    alternatives: List[Bond]
    explanation: Explanation
    projection: Optional[dict]
    required_capital: Optional[float] = None

class GoalRequest(BaseModel):
    amount: float
    target_yield: float
