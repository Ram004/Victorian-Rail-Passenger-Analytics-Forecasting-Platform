from pyspark.sql import SparkSession
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Spark
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Passenger Demand Forecast")
    .getOrCreate()
)

# --------------------------------------------------
# Read Gold Forecast Input
# --------------------------------------------------

forecast_df = (
    spark.read.parquet(
        "data/gold/gold_forecast_input"
    )
)

# Convert to pandas
pdf = forecast_df.toPandas()

# --------------------------------------------------
# Prophet Format
# --------------------------------------------------

pdf = pdf.rename(
    columns={
        "year_month": "ds",
        "total_boardings": "y"
    }
)

pdf["ds"] = pd.to_datetime(pdf["ds"])

pdf = pdf.sort_values("ds")

# --------------------------------------------------
# Train Prophet Model
# --------------------------------------------------

model = Prophet(
    yearly_seasonality=True
)

model.fit(pdf)

# --------------------------------------------------
# Forecast Next 24 Months
# --------------------------------------------------

future = model.make_future_dataframe(
    periods=24,
    freq="ME"
)

forecast = model.predict(future)

# --------------------------------------------------
# Save Forecast Data
# --------------------------------------------------

output_dir = Path("data/forecast")
output_dir.mkdir(
    parents=True,
    exist_ok=True
)

forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
].to_csv(
    output_dir / "passenger_demand_forecast.csv",
    index=False
)

# --------------------------------------------------
# Forecast Chart
# --------------------------------------------------

fig = model.plot(forecast)

plt.title(
    "Passenger Demand Forecast"
)

plt.tight_layout()

plt.savefig(
    output_dir / "passenger_demand_forecast.png"
)

plt.close()

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nFORECAST SUMMARY")
print(
    f"Historical Months: {len(pdf)}"
)

print(
    "Forecast Horizon: 24 Months"
)

print(
    "\nFiles Created:"
)

print(
    "data/forecast/passenger_demand_forecast.csv"
)

print(
    "data/forecast/passenger_demand_forecast.png"
)

spark.stop()