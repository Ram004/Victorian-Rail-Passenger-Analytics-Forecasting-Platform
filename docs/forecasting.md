# Forecasting

## Objective

Estimate network-wide monthly passenger boardings for the 24 months after the last month of data (July 2025 to June 2027), and quantify how reliable that estimate is.

## Input

- Source: `data/gold/gold_forecast_input` (Snowflake: `GOLD_FORECAST_INPUT`)
- Grain: one row per month, with total boardings
- History: July 2018 to June 2025 (84 months)

## Validation method

A 12-month holdout was used. Models were trained on the first 72 months (July 2018 to June 2024) and scored on the final 12 months (July 2024 to June 2025). Metrics are MAE, RMSE and MAPE.

The validation is implemented in `scripts/forecast.py` and written to `data/forecast/forecast_validation_metrics.csv`.

## Models compared

| Model | MAE | RMSE | MAPE |
|---|---|---|---|
| Prophet (all history) | 7.79M | 8.15M | 37.33% |
| Prophet (from July 2022) | 5.19M | 5.73M | 25.01% |
| Prophet (COVID months masked, Mar 2020 to Jun 2022) | 5.93M | 6.86M | 29.14% |
| **Seasonal naive** | **1.31M** | **1.60M** | **6.20%** |
| Seasonal naive × trailing YoY growth | 2.74M | 3.01M | 13.50% |

Seasonal naive forecasts each month as the same month one year earlier.

## Why Prophet performed poorly

The training period includes the COVID-19 collapse in 2020 to 2021. Prophet fits a trend through that period, and the trend does not describe the later recovery. Training only on the post-2022 data, or masking the COVID months, improved the result but did not beat the seasonal baseline. Only 24 months of post-July 2022 data were available for training, which limits what Prophet can learn about yearly seasonality.

## Selected model

Seasonal naive. The final forecast repeats the most recent 12 months of actuals (July 2024 to June 2025) for both forecast years, so Year 2 equals Year 1 by design.

Uncertainty band: the lower and upper bounds are the forecast multiplied by (1 − p) and (1 + p), where p is the 90th percentile of absolute percentage error of the seasonal naive method on the holdout (approximately 12.5%).

The forecast is produced by `scripts/forecast_demand.py` and written to `data/forecast/passenger_demand_forecast.csv` with columns `ds`, `yhat`, `yhat_lower`, `yhat_upper` and `model`. Only forecast months are in the file. History is plotted from `GOLD_FORECAST_INPUT` in Power BI.

## Limitations

- The forecast assumes no growth and no change from the last 12 months of actuals.
- The uncertainty band is empirical and approximate. It is based on a single 12-month holdout and likely understates uncertainty in the second forecast year.
- Passenger counts are estimated rather than directly observed.
- COVID-19 caused structural changes in travel behaviour that limit how well models trained on that period generalise.
- Public holidays, weather, population growth, major events and service changes are not modelled.

## Possible improvements

- Rolling-origin backtests across several holdout windows
- Station-level or line-level forecasts
- Calendar effects (public holidays, school terms, major events)
- A model with an explicit post-COVID level shift
