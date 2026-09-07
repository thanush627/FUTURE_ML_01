# Task 2 — Customer Churn Prediction

Scoring every telecom customer on how likely they are to cancel, so retention effort can go where it matters.

---

## The problem

Winning a new customer costs far more than keeping an existing one, but a retention team can only call so many people. A ranked list of who is most likely to leave turns a blanket campaign into a targeted one.

That makes this a **probability** problem, not a yes/no one. A customer at 0.91 and a customer at 0.52 are both "will churn" to a classifier, but only one of them is worth a call today.

## The data

`TelcoCustomerChurn.csv` — the IBM Telco Customer Churn dataset.

| | |
|---|---|
| Customers | 7,043 |
| Features | 21 |
| Churned | 1,869 (**26.5%**) |
| Retained | 5,174 (73.5%) |

Features cover demographics (gender, senior citizen, partner, dependents), account details (tenure, contract, payment method, billing), and subscribed services (phone, internet, streaming, tech support).

The classes are imbalanced roughly 3:1, which is why **accuracy alone is misleading** — a model that predicts "nobody churns" scores 73.5% and is completely useless. ROC AUC is reported alongside it for that reason.

## Method

**Preparation**
1. Drop `customerID` — an identifier carries no signal and would only invite leakage.
2. Coerce `TotalCharges` to numeric. It arrives as text with blank strings for new customers who haven't been billed yet; those become `NaN` and are filled with the median.
3. Map `Churn` from Yes/No to 1/0.
4. One-hot encode all categorical columns with `drop_first=True` to avoid the dummy variable trap.
5. Split 80/20 with `random_state=42` for reproducibility.

**Models** — three, spanning the complexity range: a linear baseline, a bagged ensemble, and a boosted one.

## Results

| Model | Accuracy | ROC AUC |
|---|:--:|:--:|
| **Logistic Regression** | **0.82** | **0.862** |
| Random Forest | 0.79 | 0.837 |
| XGBoost | 0.79 | 0.838 |

**The simplest model wins.** Logistic Regression outperforms both ensembles on accuracy and AUC. That isn't a fluke to explain away — churn here is driven by a handful of strong, largely linear signals (contract type, tenure, monthly charges), and on 7,043 rows the extra flexibility of a tree ensemble mostly fits noise. It's a useful reminder that reaching for the most powerful model is not the same as reaching for the best one.

The exported predictions come from XGBoost, which is worth revisiting given the numbers above.

## Files

| File | What it is |
|---|---|
| `futureinternsml_task_2.py` | The full pipeline, load through export |
| `TelcoCustomerChurn.csv` | Source dataset |
| `Churn_Prediction_Output.xlsx` | All 1,409 test customers with churn probabilities |
| `ChurnPredictionDashboard.pbix` | Power BI dashboard |

## Running it

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
cd "Task 2"
python futureinternsml_task_2.py
```

It prints a confusion matrix, classification report and ROC AUC per model, plots the top 10 features by importance, and writes `Churn_Prediction_Output.xlsx`.

## Reading the output

| Column | Meaning |
|---|---|
| `Churn_Probability` | Model's estimated probability of churn, 0–1 |
| `Actual` | What really happened (1 = churned) |
| `Predicted` | Class at the default 0.5 threshold |
| *(all feature columns)* | The encoded inputs behind the prediction |

Sort by `Churn_Probability` descending and you have a call list in priority order.

**The 0.5 threshold is a default, not a decision.** Lower it to catch more at-risk customers at the cost of contacting people who were never going to leave; raise it to spend less effort at the cost of missing some. The right cut-off depends on what a retention call costs versus what a lost customer costs — `Churn_Probability` is in the workbook precisely so you can make that call yourself.
