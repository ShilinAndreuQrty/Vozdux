from app.models import Bond


MOCK_BONDS = [
    Bond(ticker="SU26238RMFS6", name="ОФЗ 26238", price=101.2, yield_percent=10.5, risk=1, duration=36, issuer_rating=1, coupon=7.4, yield_to_maturity=10.3),
    Bond(ticker="SU26240RMFS",  name="ОФЗ 26240", price=98.5,  yield_percent=11.8, risk=1, duration=24, issuer_rating=1, coupon=8.1, yield_to_maturity=11.6),
    Bond(ticker="SU26242RMFS",  name="ОФЗ 26242", price=99.1,  yield_percent=11.3, risk=1, duration=18, issuer_rating=1, coupon=7.9, yield_to_maturity=11.1),
    Bond(ticker="SU29014RMFS",  name="ОФЗ-ПК 29014", price=100.4, yield_percent=10.2, risk=1, duration=12, issuer_rating=1, coupon=10.2, yield_to_maturity=10.2),
    Bond(ticker="SU26241RMFS",  name="ОФЗ 26241", price=97.8,  yield_percent=11.9, risk=1, duration=30, issuer_rating=1, coupon=8.5, yield_to_maturity=11.7),


    Bond(ticker="GAZP",  name="Газпром облигация", price=98.7, yield_percent=12.1, risk=2, duration=12, issuer_rating=2, coupon=9.5, yield_to_maturity=11.9),
    Bond(ticker="SBERB1", name="Сбербанк БО-П03", price=99.3, yield_percent=11.6, risk=2, duration=18, issuer_rating=2, coupon=9.2, yield_to_maturity=11.4),
    Bond(ticker="RSHB1", name="РСХБ 001P-08", price=96.9, yield_percent=12.8, risk=2, duration=24, issuer_rating=2, coupon=10.0, yield_to_maturity=12.5),
    Bond(ticker="RZD1",  name="РЖД 001P-28R", price=100.1, yield_percent=11.2, risk=2, duration=36, issuer_rating=2, coupon=8.9, yield_to_maturity=11.0),
    Bond(ticker="ALRS1", name="АЛРОСА 001P-02", price=95.5, yield_percent=13.2, risk=2, duration=30, issuer_rating=2, coupon=10.4, yield_to_maturity=12.9),
    Bond(ticker="MGNT1", name="Магнит БО-004Р", price=97.4, yield_percent=12.6, risk=2, duration=20, issuer_rating=2, coupon=9.8, yield_to_maturity=12.3),
    Bond(ticker="NLMK1", name="НЛМК БО-001P", price=98.2, yield_percent=12.0, risk=2, duration=16, issuer_rating=2, coupon=9.3, yield_to_maturity=11.8),
    Bond(ticker="TATN1", name="Татнефть 001P-04", price=97.1, yield_percent=12.4, risk=2, duration=22, issuer_rating=2, coupon=9.7, yield_to_maturity=12.1),
    Bond(ticker="VTB1",  name="ВТБ Б-1-347", price=101.5, yield_percent=10.9, risk=2, duration=14, issuer_rating=2, coupon=8.8, yield_to_maturity=10.7),
    Bond(ticker="MTS1",  name="МТС 001P-20", price=96.7, yield_percent=13.0, risk=2, duration=28, issuer_rating=2, coupon=10.1, yield_to_maturity=12.7),


    Bond(ticker="SELG1", name="Сегежа 002Р-01", price=93.4, yield_percent=15.2, risk=3, duration=24, issuer_rating=3, coupon=12.5, yield_to_maturity=14.9),
    Bond(ticker="AFKS1", name="АФК Система 001Р", price=92.8, yield_percent=15.6, risk=3, duration=30, issuer_rating=3, coupon=12.8, yield_to_maturity=15.3),
    Bond(ticker="POLE1", name="Полюс БО-П01", price=94.2, yield_percent=14.8, risk=3, duration=18, issuer_rating=3, coupon=12.1, yield_to_maturity=14.5),
    Bond(ticker="FIXP1", name="Fix Price БО-01", price=91.9, yield_percent=16.1, risk=3, duration=12, issuer_rating=3, coupon=13.0, yield_to_maturity=15.8),
    Bond(ticker="OKEY1", name="О'КЕЙ Финанс 001P", price=90.7, yield_percent=16.8, risk=3, duration=20, issuer_rating=3, coupon=13.5, yield_to_maturity=16.4),
]



MOCK_BONDS_BY_TICKER = {bond.ticker.upper(): bond for bond in MOCK_BONDS}
