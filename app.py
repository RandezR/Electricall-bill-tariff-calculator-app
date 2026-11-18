from flask import Flask, render_template, request
from calculator import Tarif, monthly_kwh, monthly_cost, recommend_mcb

app = Flask(__name__)

TRANSLATIONS = {
  "en": {
    "page_title": "WattWise — Electricity cost calculator",
    "choose_language": "Choose language",
    "english": "English",
    "indonesian": "Bahasa Indonesia",
    "home": "WattWise home",
    "eyebrow": "YOUR ENERGY, MADE CLEAR",
    "heading_first": "Know what your power",
    "heading_second": "is costing you.",
    "intro": "A simple way to estimate your monthly electricity use and bill. Add a few appliances to get started.",
    "setup_title": "Build your estimate",
    "setup_description": "A few details are all we need.",
    "step": "STEP 01 / 01",
    "connection": "Your electricity connection",
    "tariff_note": "Choose the capacity shown on your electricity meter or bill.",
    "appliances": "Appliances",
    "up_to": "Add as many as you need",
    "add_appliance": "Add appliance",
    "remove_appliance": "Remove appliance",
    "appliance": "Appliance",
    "name": "name",
    "placeholder": "e.g. Fan",
    "power": "POWER (W)",
    "hours": "HOURS / DAY",
    "calculate": "Calculate my bill",
    "estimate_days": "Estimates are based on 30 days of use.",
    "your_estimate": "Your estimate",
    "calculated": "CALCULATED",
    "monthly_bill": "Estimated monthly bill",
    "based_on": "Based on your selected connection and usage",
    "monthly_energy": "Monthly energy",
    "suggested_mcb": "Suggested MCB",
    "empty_heading": "Your numbers, at a glance.",
    "empty_description": "Fill in your appliances and we’ll estimate your monthly energy use and cost.",
    "estimate_note": "Estimates use configured household tariffs and are for guidance only.",
    "breakdown": "Usage breakdown",
    "appliance_singular": "appliance",
    "appliance_plural": "appliances",
    "days": "30 days",
    "hours_per_day": "hours per day",
    "per_month": "kWh/mo",
    "footer": "WattWise · A clearer view of your home energy.",
    "error_fields": "Complete the appliance name, power, and hours for each row you use.",
    "error_range": "Power must be between 0 and 100,000 W, and hours must be between 0 and 24.",
    "error_required": "Add at least one appliance to calculate your estimate.",
    "error_invalid": "Enter valid numbers for your connection and appliance usage.",
    "decimal": ".",
  },
  "id": {
    "page_title": "WattWise — Kalkulator biaya listrik",
    "choose_language": "Pilih bahasa",
    "english": "English",
    "indonesian": "Bahasa Indonesia",
    "home": "Beranda WattWise",
    "eyebrow": "ENERGI ANDA, LEBIH MUDAH DIPAHAMI",
    "heading_first": "Ketahui biaya listrik",
    "heading_second": "rumah Anda.",
    "intro": "Perkirakan pemakaian dan biaya listrik bulanan dengan mudah. Tambahkan beberapa peralatan untuk memulai.",
    "setup_title": "Buat perkiraan",
    "setup_description": "Cukup isi beberapa detail.",
    "step": "LANGKAH 01 / 01",
    "connection": "Daya listrik terpasang",
    "tariff_note": "Pilih daya yang tertera pada meteran atau tagihan listrik Anda.",
    "appliances": "Peralatan listrik",
    "up_to": "Tambahkan sesuai kebutuhan",
    "add_appliance": "Tambah peralatan",
    "remove_appliance": "Hapus peralatan",
    "appliance": "Peralatan",
    "name": "nama",
    "placeholder": "mis. Kipas",
    "power": "DAYA (W)",
    "hours": "JAM / HARI",
    "calculate": "Hitung tagihan saya",
    "estimate_days": "Perkiraan dihitung untuk pemakaian selama 30 hari.",
    "your_estimate": "Perkiraan Anda",
    "calculated": "SELESAI DIHITUNG",
    "monthly_bill": "Perkiraan tagihan bulanan",
    "based_on": "Berdasarkan daya terpasang dan pemakaian pilihan Anda",
    "monthly_energy": "Pemakaian energi bulanan",
    "suggested_mcb": "Rekomendasi MCB",
    "empty_heading": "Lihat perkiraan Anda.",
    "empty_description": "Isi daftar peralatan untuk memperkirakan pemakaian energi dan biaya bulanan.",
    "estimate_note": "Perkiraan menggunakan tarif rumah tangga yang tersedia dan hanya sebagai panduan.",
    "breakdown": "Rincian pemakaian",
    "appliance_singular": "peralatan",
    "appliance_plural": "peralatan",
    "days": "30 hari",
    "hours_per_day": "jam per hari",
    "per_month": "kWh/bln",
    "footer": "WattWise · Kenali pemakaian energi rumah Anda.",
    "error_fields": "Lengkapi nama peralatan, daya, dan jam pemakaian pada setiap baris yang diisi.",
    "error_range": "Daya harus antara 0–100.000 W dan pemakaian antara 0–24 jam.",
    "error_required": "Tambahkan minimal satu peralatan untuk menghitung perkiraan.",
    "error_invalid": "Masukkan angka yang valid untuk daya terpasang dan pemakaian peralatan.",
    "decimal": ",",
  },
}

@app.route("/", methods=["GET", "POST"])
def index():
  result = None
  error = None
  lang = request.values.get("lang", "en")
  if lang not in TRANSLATIONS:
    lang = "en"
  text = TRANSLATIONS[lang]
  form_data = {
    "va": "1300",
    "items": [{"name": "", "watt": "", "hours": ""}],
  }

  if request.method == "POST":
    names = request.form.getlist("name")
    watts = request.form.getlist("watt")
    hours_per_day = request.form.getlist("hours")
    form_data["va"] = request.form.get("va", "1300")
    form_data["items"] = [
      {"name": name.strip(), "watt": watt.strip(), "hours": hours.strip()}
      for name, watt, hours in zip(names, watts, hours_per_day)
    ]

    try:
      va = int(form_data["va"])
      if va not in Tarif:
        raise ValueError

      items = []
      for item in form_data["items"]:
        name, watt, hours = item["name"], item["watt"], item["hours"]
        if not name and not watt and not hours:
          continue
        if not name or not watt or not hours:
          raise ValueError("fields")

        watt_value, hours_value = float(watt), float(hours)
        if watt_value < 0 or watt_value > 100000 or hours_value < 0 or hours_value > 24:
          raise ValueError("range")

        items.append({
          "name": name,
          "watt": watt_value,
          "hours": hours_value,
          "kwh_month": monthly_kwh(watt_value, hours_value),
        })

      if not items:
        raise ValueError("required")

      total_kwh = sum(item["kwh_month"] for item in items)
      total_watt = sum(item["watt"] for item in items)
      result = {
        "items": items,
        "total_kwh": round(total_kwh, 1),
        "cost": round(monthly_cost(total_kwh, va)),
        "mcb": recommend_mcb(total_watt),
      }
    except ValueError as exc:
      error = text.get("error_" + str(exc), text["error_invalid"])

  return render_template(
    "index.html",
    result=result,
    error=error,
    form_data=form_data,
    lang=lang,
    t=text,
  )

if __name__ == "__main__":
    app.run(debug=True)