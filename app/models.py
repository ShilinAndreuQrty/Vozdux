from pydantic import BaseModel

#Облигация
class Bond(BaseModel):
    ticker: str
    name: str
    price: float
    yield_percent: float
    risk: int
    duration: int 

#Ввод пользователя 
class UserInput(BaseModel):
    amount : float
    risk : int 
    duration : int 