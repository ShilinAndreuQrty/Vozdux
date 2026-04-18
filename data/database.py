import pandas as pd
import numpy as np
import os
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

# Изменить рабочую директорию на папку со скриптом (если нужно)
print(os.getcwd())
#script_dir = os.path.dirname(os.path.abspath(__file__))
#os.chdir(script_dir)

# Использование функции, установка названием строк "Название" облигации
df = json_to_dataframe(json_path='data/data.json')
#df.set_index('name',inplace=True)

# Математический подсчёт рейтинга каждой облигации
#df['price_sale']=(df['price']*(df['yield_percent'])/100)/df['duration']
print(df)
#df.to_csv('pathpoint.csv')

# Подготовка к выводу, вывод конечных данных
#df.reset_index(inplace=True)
#print(df)
#df.to_json('export.json',orient='records',index=False)