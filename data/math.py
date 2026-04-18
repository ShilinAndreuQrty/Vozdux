import pandas as pd
import math
from pydantic import BaseModel

from data.database import df

arr=df.loc[:,'price':'duration'].values

k1=0.05
k2=0.02
k3=0.1
yield_percent, risk, duration_months, price = arr[:,0], arr[:,1], arr[:,2], arr[:,3]

# Нормализация доходности (перевод процентов в доли)
normalized_yield = yield_percent / 100

# Штраф за риск: квадратичная зависимость
risk_penalty = k1 * (risk ** 2)

# Штраф за дюрацию: квадратичная зависимость, нормализация на 36 месяцев (3 года)
duration_penalty = k2 * ((duration_months / 36) ** 2)

# Дисконт к номиналу (номинал = 1000 руб.)
discount = (1000 - price) / 1000

# Расчёт итогового рейтинга
rating = (
    normalized_yield *
    (1 - risk_penalty) *
    (1 - duration_penalty) +
    k3 * discount
)

df['rating'] = rating

print(df)