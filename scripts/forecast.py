from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

# ------------------------------------------
# Spark
# ------------------------------------------

spark = (
    SparkSession.builder
    .appName("Forecast Validation")
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

# ------------------------------------------
# Train/Test Split (12-month holdout)
# ------------------------------------------

train = pdf.iloc[:-12]
test = pdf.iloc[-12:]
actuals = test["y"].values

print(f"Train: {train['ds'].min().date()} to {train['ds'].max().date()} ({len(train)} months)")
print(f"Test : {test['ds'].min().date()} to {test['ds'].max().date()} ({len(test)} months)")

# ------------------------------------------
# Helpers
# ------------------------------------------

def score(pred):
    mae = mean_absolute_error(actuals, pred)
    rmse = np.sqrt(mean_squared_error(actuals, pred))
    mape = np.mean(np.abs((actuals - pred) / actuals)) * 100
    return mae, rmse, mape


def prophet_pred(train_df):
    m = Prophet(yearly_seasonality=True)
    m.fit(train_df)
    fc = m.predict(test[["ds"]])  # predict exactly the holdout dates
    return fc["yhat"].values

# ------------------------------------------
# Models
# ------------------------------------------

# 1) Prophet trained on all history before the holdout
pred_full = prophet_pred(train)

# 2) Prophet trained on the post-COVID window only (July 2022 onwards)
pred_post = prophet_pred(train[train["ds"] >= "2022-07-01"])

# 3) Prophet with COVID months masked out (Mar 2020 - Jun 2022)
train_masked = train.copy()
mask = (train_masked["ds"] >= "2020-03-01") & (train_masked["ds"] <= "2022-06-01")
train_masked.loc[mask, "y"] = np.nan
pred_masked = prophet_pred(train_masked)

# 4) Seasonal naive: same month one year earlier
pred_naive = pdf.iloc[-24:-12]["y"].values

# 5) Seasonal naive scaled by trailing year-on-year growth
#    growth = last 12 months of training / the 12 months before that
last12 = train["y"].iloc[-12:].sum()
prev12 = train["y"].iloc[-24:-12].sum()
growth = last12 / prev12
pred_naive_growth = pred_naive * growth
print(f"\nTrailing YoY growth factor used: {growth:.3f}")

results = {
    "Prophet (all history)": score(pred_full),
    "Prophet (from Jul 2022)": score(pred_post),
    "Prophet (COVID masked)": score(pred_masked),
    "Seasonal naive": score(pred_naive),
    "Seasonal naive x YoY growth": score(pred_naive_growth),
}

metrics_df = pd.DataFrame(
    [(name, *vals) for name, vals in results.items()],
    columns=["model", "MAE", "RMSE", "MAPE"],
)

# ------------------------------------------
# Save Results
# ------------------------------------------

output_dir = Path("data/forecast")
output_dir.mkdir(parents=True, exist_ok=True)

metrics_df.to_csv(output_dir / "forecast_validation_metrics.csv", index=False)

# ------------------------------------------
# Summary
# ------------------------------------------

print("\nFORECAST VALIDATION (holdout: last 12 months)")
print("---------------------------------------------")
print(metrics_df.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

spark.stop()