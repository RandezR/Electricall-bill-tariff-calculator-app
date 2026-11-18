from calculator import daily_kwh, monthly_kwh, monthly_cost, recommend_mcb

def test_daily_kwh():
    assert daily_kwh(100, 10) == 1.0

def test_monthly_kwh():
    assert round(monthly_cost(100, va=1300), 2) == 144470.0

def test_recommend_mcb():
    assert recommend_mcb(1000) == 10