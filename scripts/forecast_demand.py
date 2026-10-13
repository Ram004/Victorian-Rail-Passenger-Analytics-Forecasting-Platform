from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------
# Spark
# ------------------------------------------

spark = (
    SparkSession.builder
    .appName("Passenger Demand Forecast")
    .getOrCreate()
)

# ------------------------------------------
# Read Gold Forecast Input
# ------------------------------------------

forecast_df = spark.read.parquet("data/gold/gold_forecast_input")
pdf = forecast_df.toPandas()

pdf = pdf.rename(columns={"year_month": "ds", "total_boardings": "y"})
pdf["ds"] = pd.to_datetime(pdf["ds"])
pdf = pdf.sort_values("ds").reset_index(drop=True)

HORIZON = 24

# ------------------------------------------
# Uncertainty band from the 12-month holdout
# (seasonal naive: same month one year earlier)
# ------------------------------------------

holdout_actual = pdf["y"].iloc[-12:].values
holdout_pred = pdf["y"].iloc[-24:-12].values
abs_pct_err = np.abs((holdout_actual - holdout_pred) / holdout_actual)
band = float(np.quantile(abs_pct_err, 0.90))

# ------------------------------------------
# Seasonal naive forecast: repeat the last 12 months
# ------------------------------------------

last12 = pdf["y"].iloc[-12:].values
last_date = pdf["ds"].max()

future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthBegin(1),
    periods=HORIZON,
    freq="MS",
)

yhat = np.array([last12[i % 12] for i in range(HORIZON)], dtype=float)

forecast = pd.DataFrame({
    "ds": future_dates,
    "yhat": yhat,
    "yhat_lower": yhat * (1 - band),
    "yhat_upper": yhat * (1 + band),
    "model": "Seasonal naive",
})

# ------------------------------------------
# Save
# ------------------------------------------

output_dir = Path("data/forecast")
output_dir.mkdir(parents=True, exist_ok=True)

forecast.to_csv(output_dir / "passenger_demand_forecast.csv", index=False)

# ------------------------------------------
# Chart
# ------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(pdf["ds"], pdf["y"], label="Actual boardings")
ax.plot(forecast["ds"], forecast["yhat"], linestyle="--", label="Forecast (seasonal naive)")
ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"], alpha=0.2, label="Uncertainty band")
ax.set_title("Monthly Passenger Boardings: Actual and Forecast")
ax.set_ylabel("Boardings")
ax.legend()
fig.tight_layout()
fig.savefig(output_dir / "passenger_demand_forecast.png", dpi=150)

# ------------------------------------------
# Summary
# ------------------------------------------

print("\nFORECAST SUMMARY")
print(f"Historical months : {len(pdf)} ({pdf['ds'].min().date()} to {pdf['ds'].max().date()})")
print(f"Forecast months   : {HORIZON} ({future_dates.min().date()} to {future_dates.max().date()})")
print(f"Uncertainty band  : +/- {band:.1%} (90th percentile holdout error)")
print("\nFiles created:")
print("data/forecast/passenger_demand_forecast.csv")
print("data/forecast/passenger_demand_forecast.png")

spark.stop()