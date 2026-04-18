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
    issuer_rating : int

#Ввод пользователя 
class UserInput(BaseModel):
    amount : float
    risk : int 
    duration : int 


class Projection(BaseModel):
    estimated_lots: int
    invested_amount: float
    estimated_annual_income: float


class AnalyzeResponse(BaseModel):
    best_bond: Optional[Bond]
    alternatives: List[Bond]
    explanation: str
    projection: Optional[Projection] = None