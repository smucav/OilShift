# OilShift: Brent Oil Price Change Point Analysis

## 📈 Project Overview

OilShift explores how major geopolitical and economic events influence Brent oil prices (1987–2022) using **Bayesian change point detection**. The goal is to deliver actionable insights for investors, policymakers, and energy firms facing oil market volatility.

* **Task 1**: Robust EDA and data preparation ✅
* **Task 2**: Bayesian modeling (PyMC3) ✅
* **Task 3**: Interactive dashboard (Flask + React) 🔜

---

## 🗂️ Repository Structure

```
OilShift/
├── data/
│   ├── raw/
│   │   ├── BrentOilPrices.csv
│   │   └── key_events.csv
│   └── processed/
│       ├── brent_oil_prices_cleaned.csv
│       └── log_returns.csv
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── scripts/
│   └── data_preprocessing.py
│
├── results/
│   ├── plots/
│   │   ├── raw_price_trend.png
│   │   ├── log_returns.png
│   │   ├── volatility.png
│   │   └── price_with_events.png
│   └── summary_table.csv
│
├── docs/
│   └── interim_report.pdf
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

1️⃣ **Clone the repository:**

```bash
git clone https://github.com/your-username/OilShift.git
cd OilShift
```

2️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

> 📦 **Dependencies:** pandas==2.0.3, numpy==1.24.3, matplotlib==3.7.2, seaborn==0.12.2, statsmodels==0.14.0

3️⃣ **Verify data:**
Ensure `data/raw/BrentOilPrices.csv` and `data/raw/key_events.csv` exist.

4️⃣ **Run EDA notebook:**

```bash
jupyter notebook notebooks/01_eda.ipynb
```

Outputs are saved to `data/processed/` and `results/`.

---

## 🔍 Task 1: EDA Summary

* **Price Series:** Non-stationary. ADF: -1.9939 (p = 0.2893). Peaks (2008 \~\$143.95), drops (2014, 2020).
* **Log Returns:** Stationary. ADF: -16.4271 (p < 0.0001). Used for volatility insights.
* **Volatility:** 30-day rolling std shows clustering during crises (2008, 2020).
* **Events:** 12 key events overlaid for context.

**Summary Stats:**

| Metric             | Value    |
| ------------------ | -------- |
| Mean Price         | \$48.42  |
| Std Dev Price      | \$32.86  |
| Min Price          | \$9.10   |
| Max Price          | \$143.95 |
| Mean Log Return    | 0.000179 |
| Std Dev Log Return | 0.025532 |
| Total Rows         | 9,011    |

See `results/plots/` and `results/summary_table.csv` for visuals and details.

---

## 🧠 Task 2: Bayesian Change Point Modeling

**Model**: Implemented in PyMC 5.25.1 using continuous Beta priors for change point locations (tau) on semi-annual log returns (~70 points). Detects 2 change points to optimize convergence and runtime.


* **Outputs**:

* `results/change_point_results.csv`: Change point indices, dates, and posterior probabilities.
* `results/plots/change_points.png`: Log returns with change points and events.
* `results/plots/posterior_diagnostics.png`: Posterior distributions of model parameters.
* `results/plots/trace_diagnostics.png`: Trace plots for convergence diagnostics.

* **Diagnostics**: Targeting 0 divergences, R-hat < 1.1, ESS > 400 (run `notebooks/02_change_point_model.ipynb` to verify).

* **Implementation**: See `notebooks/02_change_point_model.ipynb` and `scripts/change_point_model.py`.

**Note**: Previous runs with monthly subsampling (~427 points) detected change points around 2001-12-31, 2007-12-31, and 2009-06-30, aligning with events like the 2003 Iraq invasion and 2008 financial crisis. Semi-annual subsampling reduces runtime while preserving key trends.


## 🗓️ Next Steps

* [ ] **Task 3:** Flask/React interactive dashboard

---

## 📚 Data Sources

* **Brent Oil Prices:** EIA or equivalent
* **Key Events:** Compiled from OPEC, EIA, BBC, Reuters

## 📬 Contact

*Questions?* Reach out at \[smucav@gmail.com].
