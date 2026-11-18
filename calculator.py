Tarif = {
  900: 1352.00,
  1300: 1444.70,
  2200: 1444.70,
  3500: 1699.53,
}

MCB_rating = [2,4,6,10,16,20,25,32,40,50,63,]

def daily_kwh(watt,hours):
    return (watt * hours) / 1000

def monthly_kwh(watt, hours, days =30):
    return daily_kwh(watt, hours) * days

def monthly_cost(total_kwh, va=1300):
    return   total_kwh * Tarif[va]

def total_current(total_watt, voltage=220, power_factor=0.85):
    return total_watt / (voltage * power_factor)

def recommend_mcb(total_watt):
    needed = total_current(total_watt) * 1.25
    for rating in MCB_rating:
        if rating >= needed:
            return rating
    return None