import pandas as pd
import numpy as np
import json

def json_to_dataframe(json_path=None, json_data=None):
    """
    Преобразует JSON в DataFrame.
    Можно передать путь к файлу или уже загруженные данные.
    """
    try:
        if json_path:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json_data

        # Если данные — список объектов
        if isinstance(data, list):
            df = pd.DataFrame(data)
        # Если данные содержат вложенную структуру
        elif isinstance(data, dict) and 'bonds' in data:
            df = pd.json_normalize(data['bonds'])
        else:
            # Универсальный вариант
            df = pd.json_normalize(data)

        return df

    except Exception as e:
        print(f"Ошибка при преобразовании JSON: {e}")
        return pd.DataFrame()

# Использование функции, установка названием строк "Название" облигации
df = json_to_dataframe(json_path='data/data.json')

# Подготовка к выводу, вывод конечных данных
#print(df)
#df.to_json('export.json',orient='records',index=False)

values=[]
for i in range(len(df['name'])):
    values.append(float(i))
df['rating']= values

#### Таблица 'топ', сравнение со всеми по параметрам

df=df[['name','ticker','duration','price','yield_percent','risk','rating']]

top_df=pd.DataFrame({
    'name':[],
    'ticker':[],
    'dur':[],
    'top_price':[],
    'top_yield_percent':[],
    'top_risk':[],
    'top_rating':[]
})
# Создаём top_df на основе df
top_df = df[['name', 'ticker', 'duration']].copy()
# Добавляем столбцы для рангов и заполняем их
starie = ['top_price', 'top_yield_percent', 'top_risk', 'top_rating']
novie = ['price', 'yield_percent', 'risk', 'rating']
top_df[starie] = df[novie].rank()

#print(top_df)

po=pd.Series(top_df.iloc[0,:])
explanation = (
        f"Выбрана облигация {po.get('name','')} ({po.get('ticker','')}) с рейтингом {po.get('top_rating'):.4f}. "
        f"Доходность {po.get('top_yield_percent')}%, риск {po.get('top_risk')}, сроком на {po.get('duration')} мес.\n"
        "Наивысшее соотношение между доходностью, риском и сроком\n"
)
#вывод
names=pd.Series(top_df['name'])
print(names)
op=names[2]
cher=df['name'].str.contains(op,case=False)
ex_r=pd.Series(top_df.iloc[cher,:])
example_rating=(
    f"Выбрана облигация {ex_r.get('name','')} ({ex_r.get('ticker','')})\n"
    "Рейтинг по критериям:\n"
    f"  - По рейтингу: {ex_r.get('top_rating'):.4f}. \n"
    f"  - По доходности: {ex_r.get('top_yield_percent')}%\n"
    f"  - По риску: {ex_r.get('top_risk')}\n"
)
#### Конец

#print(example_rating)
#pd.to_json()

