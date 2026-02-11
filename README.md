[![Live Demo](https://img.shields.io/badge/Live-Demo-orange)](https://pavellakov-streamlit-mortgage-calculator.hf.space/)





# Mortgage Calculator (Streamlit)

A Streamlit app that estimates a mortgage’s **monthly payment breakdown** and generates an **amortization schedule** (with optional extra monthly payments).

## Features
- Inputs for:
  - Home price
  - Down payment (amount and %)
  - Loan term (5/10/15/20/30 years)
  - Interest rate
  - Optional: property tax rate, homeowners insurance, HOA fees
- **Monthly payment breakdown** (Principal & Interest / Tax / Insurance / HOA) with a donut chart
- **Amortization schedule table**
- Optional **extra monthly payment** to see:
  - Total interest paid
  - Payoff time (months)
  - Cumulative principal vs. interest chart

## Tech Stack
- Python
- Streamlit
- Pandas / NumPy
- Plotly + Matplotlib

## Run Locally

### 1) Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows
```

### 2) Install dependencies
```bash
pip install streamlit pandas numpy matplotlib plotly
```

### 3) Start the app
```bash
streamlit run "Mortgage Calculator.py"
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## Project Structure (suggested for GitHub)
```
mortgage-calculator/
  Mortgage Calculator.py
  README.md
  requirements.txt
```

### Example `requirements.txt`
```txt
streamlit
pandas
numpy
matplotlib
plotly
```

## Notes
- The app uses a standard fixed-rate mortgage payment formula.
- ZIP code is collected as an input but not used for external rate/tax lookups (no API calls in this version).

## License
Add a license if you plan to publish publicly (MIT is common for small demo projects).
