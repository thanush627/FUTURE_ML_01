# Task 1 — Sales Forecasting with Prophet

Forecasting daily retail sales 90 days into the future, and presenting it as a Power BI dashboard a business user can actually read.

---

## The problem

A retailer planning staffing, stock, and cash flow needs to know what next quarter looks like. Sales data is noisy — it swings by day of week, spikes around holidays, and drifts over the year. Reading a trend off a raw line chart doesn't work, because the weekly cycle drowns out everything else.

Prophet separates those effects, so the underlying trend becomes visible and the future becomes estimable with a confidence range attached.

## The data

`task1futureinters.csv` — the Rossmann store sales dataset.

| | |
|---|---|
| Records | 1,017,209 |
| Stores | 1,115 |
| Period | 1 Jan 2013 → 31 Jul 2015 |
| Columns | `Store`, `DayOfWeek`, `Date`, `Sales`, `Customers`, `Open`, `Promo`, `StateHoliday`, `SchoolHoliday` |

Rows are per store per day. Summing sales across all stores for each date collapses this into a single company-wide series of **942 daily observations** — the level a Prophet model is fitted at.

## Method

1. **Parse dates** with an explicit `%d-%m-%Y` format. Left to infer, pandas silently misreads day-first dates as month-first and scrambles the series.
2. **Aggregate to a daily total** — `groupby('Date')['Sales'].sum()`.
3. **Rename to Prophet's schema** — it requires the columns be named `ds` (date) and `y` (value).
4. **Fit the model:**
   - `yearly_seasonality=True` — captures the annual retail cycle
   - `weekly_seasonality=True` — the strongest pattern in the data
   - `daily_seasonality=False` — meaningless at daily granularity
   - German public holidays, matching where Rossmann trades
5. **Forecast 90 days** beyond the data.
6. **Export** `ds`, `yhat`, `yhat_lower`, `yhat_upper` joined to the actuals, for Power BI.

## Files

| File | What it is |
|---|---|
| `FutureInternsML_Task_1.ipynb` | The full pipeline, load through export |
| `task1futureinters.csv` | Source dataset |
| `sales_forecast_output.xlsx` | Forecast with confidence bounds and actuals |
| `Future_Interns_ML_Task-1(Power_BI).pbix` | Power BI dashboard |

## Running it

```bash
pip install pandas prophet matplotlib openpyxl
jupyter notebook FutureInternsML_Task_1.ipynb
```

The notebook was written in Colab and reads from `/content/`. Running locally, point the `read_csv` path at `task1futureinters.csv` in this folder.

> **Prophet installation** compiles a Stan backend and can take several minutes. On Windows, `conda install -c conda-forge prophet` is usually less painful than pip.

## Reading the output

| Column | Meaning |
|---|---|
| `ds` | Date |
| `yhat` | Forecast sales |
| `yhat_lower` / `yhat_upper` | 80% confidence interval |
| `y` | Actual sales — blank for future dates |

The gap between `yhat_lower` and `yhat_upper` is the honest part of the forecast: it widens as predictions extend further out, and treating `yhat` as a single certain number ignores that.

## Notes

- **The exported workbook is a windowed slice**, not the full fit — 110 days of history plus the 90 forecast days, which is what the dashboard visualises. Re-running the export cell writes the complete series if you want it.
- **The holiday calendar is set to Germany** (`country_name='DE'`). Rossmann is a German retailer, so its closures and holiday spikes follow that calendar — an earlier version used Indian holidays, which don't align with anything in this data.
