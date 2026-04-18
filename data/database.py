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

#print(df)
#df.to_csv('pathpoint.csv')

# Подготовка к выводу, вывод конечных данных
#print(df)
#df.to_json('export.json',orient='records',index=False)

#exlanation
values=[]
for i in range(len(df['name'])):
    values.append(i)
df['rating']= values
po=pd.Series(df.iloc[0,:])
result=po

explanation = (
        f"Выбрана облигация {df.get('name','')} ({df.get('ticker','')}) с рейтингом {df.get('rating'):.4f}. "
        f"Доходность {df.get('yield_percent')}%, риск {df.get('risk')}, сроком на {df.get('duration')} мес."
)
print(explanation)
pd.to_json()