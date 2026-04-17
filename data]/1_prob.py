import requests

# Токен доступа
token = "t.n1x1VAXwKmTf5677HuAs2oRlseCqrZT5c9-MR_nKI721QQMEJ8T805bf7e3ovKIWhM260TaC64kGNqrrxBGsGw"

# URL эндпоинта
url = "https://invest-public-api.tbank.ru:443/tinkoff.public.invest.api.contract.v1.InstrumentsService/Bonds"

# Заголовки запроса
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Тело запроса
payload = {
    "instrument_status": "INSTRUMENT_STATUS_BASE",
    "page": 1,
    "per_page": 100
}

# Отправка POST‑запроса
response = requests.post(url, headers=headers, json=payload)


# Обработка ответа
if response.status_code == 200:
    data = response.json()
    print("✅ Успешный запрос! Получено облигаций:", len(data.get("bonds", [])))
    print("\n" + "="*80)
    print("СПИСОК ОБЛИГАЦИЙ:")
    print("="*80)

    # Выводим информацию по каждой облигации (первые 10 для примера)
    for i, bond in enumerate(data["bonds"][:10], 1):
        print(f"\n{i}. {bond['name']}")
        print(f"   Тикер: {bond.get('ticker', 'N/A')}")
        print(f"   FIGI: {bond.get('figi', 'N/A')}")
        print(f"   ISIN: {bond.get('isin', 'N/A')}")
        print(f"   Класс: {bond.get('class_code', 'N/A')}")
        print(f"   Лот: {bond.get('lot', 'N/A')} шт.")
        print(f"   Валюта: {bond.get('currency', 'N/A')}")
        print(f"   Погашение: {bond.get('maturity_date', 'N/A').split('T')[0]}")
        nominal = bond.get('nominal', {})
        print(f"   Номинал: {nominal.get('units', 0) + nominal.get('nano', 0) / 1_000_000_000} {bond.get('currency', '')}")
else:
    print(f"❌ Ошибка: {response.status_code}")
    print(f"Текст ошибки: {response.text}")
