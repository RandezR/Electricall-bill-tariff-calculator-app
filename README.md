# WattWise: Electricity Bill & Tariff Calculator

A simple web app that estimates your **monthly electricity usage and bill** from the appliances you use, and suggests a suitable **MCB (circuit breaker) rating**. Built with Python and Flask, with an optional desktop wrapper.

The interface is available in **English** and **Bahasa Indonesia**.

## Features

- Estimate monthly energy use (kWh) and cost from a list of appliances
- Add as many appliances as you need (name, power in watts, hours per day)
- Choose your installed connection capacity (900 / 1300 / 2200 / 3500 VA)
- Get a recommended MCB rating based on your total load
- Per-appliance usage breakdown
- Input validation with clear error messages
- Bilingual UI (English / Bahasa Indonesia)
- Optional desktop window via `pywebview`

## How It Works

All calculations live in `calculator.py`.

| Step | Formula |
|------|---------|
| Daily energy | `kWh/day = (watt × hours) / 1000` |
| Monthly energy | `kWh/month = kWh/day × 30` |
| Monthly cost | `cost = total kWh × tariff per kWh` |
| Total current | `I = watt / (220 V × 0.85 power factor)` |
| MCB size | `I × 1.25` safety margin, rounded up to the next standard rating |

**Tariff per kWh (by connection capacity):**

| Connection | Rate (per kWh) |
|-----------|----------------|
| 900 VA | 1,352.00 |
| 1300 VA | 1,444.70 |
| 2200 VA | 1,444.70 |
| 3500 VA | 1,699.53 |

**Standard MCB ratings:** 2, 4, 6, 10, 16, 20, 25, 32, 40, 50, 63 A

**Example:** a 100 W appliance used 10 hours a day consumes 1 kWh/day, or 30 kWh/month. On a 1300 VA connection that costs 30 × 1,444.70 = 43,341.

> Estimates assume 30 days of use and the configured household tariffs. They are for guidance only and may differ from your actual bill.

## Project Structure

```
.
├── app.py            # Flask app: routes, form handling, validation, translations
├── calculator.py     # Tariff table and calculation functions
├── desktop.py        # Runs the Flask app inside a desktop window (pywebview)
├── desktop.spec      # PyInstaller spec for building the desktop executable
├── main.py           # Unit tests for the calculator functions
├── assets/
│   └── WattWise.ico  # Windows desktop executable icon
├── LICENSE.txt       # MIT License
├── templates/        # HTML templates (index.html)
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8 or newer
- `pip`

### Installation

```bash
git clone https://github.com/RandezR/Electricall-bill-tariff-calculator-app.git
cd Electricall-bill-tariff-calculator-app

# (optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install flask
```

### Run the web app

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

To switch language, use the language selector in the UI or add `?lang=id` (Bahasa Indonesia) or `?lang=en` (English) to the URL.

### Run as a desktop app (optional)

```bash
pip install pywebview
python desktop.py
```

This starts the Flask server on port 5000 and opens it in a native window.

To package it as an executable (optional):

```bash
pip install pyinstaller
python -m PyInstaller --noconfirm desktop.spec
```

On Windows, the executable is created at `dist/WattWise.exe`.

### Run the tests

```bash
pip install pytest
pytest main.py
```

## Usage

1. Select your electricity connection capacity (shown on your meter or bill).
2. Add your appliances: name, power (W), and hours of use per day.
3. Click **Calculate my bill**.
4. Review the estimated monthly bill, monthly energy (kWh), suggested MCB, and usage breakdown.

## Customizing Tariffs

Edit the `Tarif` dictionary in `calculator.py` to update rates or add new connection capacities:

```python
Tarif = {
    900: 1352.00,
    1300: 1444.70,
    2200: 1444.70,
    3500: 1699.53,
}
```

If you add a new capacity, also add it to the connection options in `templates/index.html`.

## Input Limits

- Power: 0 to 100,000 W
- Usage: 0 to 24 hours per day
- At least one complete appliance row is required

## Tech Stack

- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [pywebview](https://pywebview.flowrl.com/) (desktop wrapper, optional)
- [PyInstaller](https://pyinstaller.org/) (packaging, optional)

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE.txt). You may use, copy, modify, distribute, sublicense, and sell the software, provided the copyright and permission notice are included with copies or substantial portions of the software. The software is provided "as is", without warranty.
