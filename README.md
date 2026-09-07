<div align="center">

# Future Interns — Machine Learning Internship

**Three end-to-end machine learning projects: forecasting, classification, and conversational AI.**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-337AB7)](https://xgboost.readthedocs.io/)
[![Prophet](https://img.shields.io/badge/Prophet-4267B2)](https://facebook.github.io/prophet/)
[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Dialogflow](https://img.shields.io/badge/Dialogflow-FF9800?logo=dialogflow&logoColor=white)](https://cloud.google.com/dialogflow)

</div>

---

## Overview

Each task takes a real dataset or platform through the full cycle — preparation, modelling, evaluation, and a deliverable someone can actually use, whether that's an interactive dashboard or a working chatbot.

| | Project | Problem | Approach | Deliverable |
|:--:|---|---|---|---|
| **1** | [Sales Forecasting](#task-1--sales-forecasting) | What will sales be over the next quarter? | Prophet time-series model | 90-day forecast + Power BI dashboard |
| **2** | [Customer Churn Prediction](#task-2--customer-churn-prediction) | Which customers are about to leave? | Logistic Regression · Random Forest · XGBoost | Scored customer list + Power BI dashboard |
| **3** | [Customer Support Chatbot](#task-3--customer-support-chatbot) | Answer support questions automatically | Dialogflow ES intents | Web, Telegram, and notebook interfaces |

---

## Task 1 — Sales Forecasting

**Predicting daily retail sales 90 days ahead.**

Built on the Rossmann store dataset — **1,017,209 records** across **1,115 stores**, spanning **1 Jan 2013 to 31 Jul 2015**. Individual store rows are aggregated into a single **942-day** company-wide daily series, which Prophet decomposes into trend, yearly and weekly seasonality, and holiday effects.

Weekly seasonality matters here: retail sales swing hard between weekdays and weekends, and a model that ignores that pattern spends its error budget re-learning the same cycle every week.

**Output** — a 90-day forecast with `yhat_lower`/`yhat_upper` confidence bounds, exported to Excel and visualised in Power BI alongside the actuals.

📁 [`Task 1/`](Task%201) — notebook, dataset, forecast workbook, `.pbix` dashboard

---

## Task 2 — Customer Churn Prediction

**Identifying telecom customers likely to cancel.**

Built on the Telco Customer Churn dataset — **7,043 customers**, **21 features**, with **26.5% churn** (1,869 of 7,043). Categorical fields are one-hot encoded, `TotalCharges` is coerced to numeric and median-imputed, and the data is split 80/20.

Three models are trained and compared:

| Model | Accuracy | ROC AUC |
|---|:--:|:--:|
| **Logistic Regression** | **0.82** | **0.862** |
| Random Forest | 0.79 | 0.837 |
| XGBoost | 0.79 | 0.838 |

A useful result worth stating plainly: **the simplest model wins.** Logistic Regression beats both tree ensembles on this dataset — churn here is driven by largely linear, well-separated signals such as contract type and tenure, and the extra capacity of the ensembles buys nothing but variance. It is the model that ships.

**Output** — every test customer scored with a churn probability, exported to Excel and turned into a Power BI dashboard.

📁 [`Task 2/`](Task%202) — script, dataset, scored workbook, `.pbix` dashboard

---

## Task 3 — Customer Support Chatbot

**A support bot that answers customer questions across three channels.**

Intent matching is handled by **Dialogflow ES**, with three separate front-ends sharing one agent:

| Interface | File | Use |
|---|---|---|
| 🌐 **Web app** | `chatbot_app.py` | Streamlit chat UI |
| 💬 **Telegram** | `telegrambot_py.py` | Chat with the bot from your phone |
| 📓 **Notebook** | `dialogflowbot.py` | Inline widget for Colab testing |

📁 [`Task 3/`](Task%203) — all three interfaces plus a demo recording

---

## Getting started

```bash
git clone https://github.com/thanush627/FUTURE_ML_01.git
cd FUTURE_ML_01
pip install pandas numpy scikit-learn xgboost prophet matplotlib seaborn openpyxl
```

Then follow the README inside whichever task folder you want to run — each has its own setup steps, since Task 3 additionally needs Google Cloud credentials.

> **Note on the `.pbix` files** — the Power BI dashboards read the Excel workbooks in their folders. If you regenerate a workbook, refresh the dashboard in Power BI Desktop to pick up the new numbers.

---

## Tech stack

| Area | Tools |
|---|---|
| Data | pandas · NumPy |
| Forecasting | Prophet |
| Classification | scikit-learn · XGBoost |
| Visualisation | Matplotlib · Seaborn · Power BI |
| Conversational AI | Dialogflow ES · Streamlit · python-telegram-bot |

---

## Author

**Thanush**
