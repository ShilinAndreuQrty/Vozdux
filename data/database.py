import pandas as pd
import numpy as np  
import json

# Функция для дюрации
def calculate_bond_duration(arr):
    yield_percent = arr[:, 4]
    maturity_months = arr[:, 2]
    
    macaulay_duration_months = maturity_months
    macaulay_duration_years = maturity_months / 12

    # Модифицированная дюрация
    modified_duration = macaulay_duration_years / (1 + yield_percent / 100)
    # Изменение цены при изменении доходности на 1 %
    price_change_percent = modified_duration * 100

    return price_change_percent

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
# Смена порядка колонок
df=df[['name','ticker','duration','price','yield_percent','risk','rating']]
# Создание новой таблички
top_df=pd.DataFrame({
    'name':[],
    'ticker':[],
    'dur':[],
    'top_price':[],
    'top_yield_percent':[],
    'top_duration':[],
    'top_rating':[]
})
# Создаём top_df на основе df
top_df = df[['name', 'ticker', 'duration']].copy()
top_df['top_duration']=calculate_bond_duration(df.values)
print(top_df)
# Добавляем столбцы для рангов и заполняем их
novie = ['top_price', 'top_yield_percent', 'top_rating']
starie = ['price', 'yield_percent', 'rating']
top_df[novie] = df[starie].rank()

# Выбор строчки с информацией и вывод текста
names=pd.Series(df['name'])
ap=names[2] # число - индекс имени, в списке прошлом, просто для поиска
cher2=(df[df['name']==ap]).index[0]
po=pd.Series(df.loc[cher2,:])
explanation = (
        f"Выбрана облигация {po.get('name','')} ({po.get('ticker','')}) с рейтингом {po.get('rating'):.4f}. "
        f"Доходность {po.get('yield_percent')}%, риск {po.get('risk')}, сроком на {po.get('duration')} мес.\n"
        "Наивысшее соотношение между доходностью, риском и сроком\n"
)

# Нахождение индекса нужной строчки по названию облигации и вывод текста с информацией из рейтинга: top_df
names=pd.Series(top_df['name'])
op=names[2] # число - индекс имени, в списке прошлом, просто для поиска
cher=(top_df[top_df['name']==op]).index[0]
ex_r=pd.Series(top_df.loc[cher,:])
example_rating=(
    f"Выбрана облигация {ex_r.get('name','')} ({ex_r.get('ticker','')})\n"
    "Рейтинг по критериям:\n"
    f"  - По рейтингу: {ex_r.get('top_rating'):.4f}. \n"
    f"  - По доходности: {ex_r.get('top_yield_percent')}\n"
    f"  - По дюрации: {ex_r.get('top_duration')}\n"
)
#### Конец

print(example_rating)