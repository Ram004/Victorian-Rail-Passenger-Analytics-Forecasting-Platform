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

forecast_df = spark.read.parquet(
    "data/gold/gold_forecast_input"
)

pdf = forecast_df.toPandas()

pdf = pdf.rename(
    columns={
        "year_month": "ds",
        "total_boardings": "y"
    }
)

pdf["ds"] = pd.to_datetime(pdf["ds"])
pdf = pdf.sort_values("ds")

# ------------------------------------------
# Train/Test Split
# ------------------------------------------

train = pdf.iloc[:-12]
test = pdf.iloc[-12:]

# ------------------------------------------
# Train Model
# ------------------------------------------

model = Prophet(
    yearly_seasonality=True
)

model.fit(train)

# ------------------------------------------
# Predict Last 12 Months
# ------------------------------------------

future = model.make_future_dataframe(
    periods=12,
    freq="ME"
)

forecast = model.predict(future)

predictions = forecast.tail(12)["yhat"].values
actuals = test["y"].values

# ------------------------------------------
# Metrics
# ------------------------------------------

mae = mean_absolute_error(
    actuals,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        actuals,
        predictions
    )
)

mape = (
    np.mean(
        np.abs(
            (actuals - predictions)
            / actuals
        )
    ) * 100
)

# ------------------------------------------
# Save Results
# ------------------------------------------

output_dir = Path("data/forecast")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)

metrics_df = pd.DataFrame({
    "metric": [
        "MAE",
        "RMSE",
        "MAPE"
    ],
    "value": [
        mae,
        rmse,
        mape
    ]
})

metrics_df.to_csv(
    output_dir / "forecast_validation_metrics.csv",
    index=False
)

# ------------------------------------------
# Summary
# ------------------------------------------

print("\nFORECAST VALIDATION")
print("--------------------------")
print(f"MAE : {mae:,.0f}")
print(f"RMSE: {rmse:,.0f}")
print(f"MAPE: {mape:.2f}%")

spark.stop()