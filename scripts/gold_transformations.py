from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    avg,
    max,
    date_format,
    year
)

# ---------------------------------------------------------------------
# Spark Session
# ---------------------------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Metro Gold Transformations")
    .config("spark.driver.memory", "16g")
    .config("spark.executor.memory", "16g")
    .getOrCreate()
)

# ---------------------------------------------------------------------
# Read Silver Tables
# ---------------------------------------------------------------------

fact_df = spark.read.parquet(
    "data/silver/fact_passenger_counts"
)

line_df = spark.read.parquet(
    "data/silver/dim_line"
)

print(f"Fact Rows: {fact_df.count():,}")

# ---------------------------------------------------------------------
# GOLD_PASSENGER_DEMAND
# Monthly demand by line
# ---------------------------------------------------------------------

gold_passenger_demand = (
    fact_df
    .groupBy(
        "source_financial_year",
        date_format("Business_Date", "yyyy-MM").alias("year_month"),
        "Line_Name"
    )
    .agg(
        sum("Passenger_Boardings").alias("total_boardings"),
        sum("Passenger_Alightings").alias("total_alightings")
    )
    .withColumn(
        "total_passenger_activity",
        col("total_boardings") + col("total_alightings")
    )
)

# ---------------------------------------------------------------------
# GOLD_STATION_DEMAND
# ---------------------------------------------------------------------

gold_station_demand = (
    fact_df
    .groupBy(
        "Station_Name",
        date_format("Business_Date", "yyyy-MM").alias("year_month")
    )
    .agg(
        sum("Passenger_Boardings").alias("total_boardings"),
        sum("Passenger_Alightings").alias("total_alightings")
    )
)

# ---------------------------------------------------------------------
# GOLD_LINE_GROWTH
# ---------------------------------------------------------------------

gold_line_growth = (
    fact_df
    .groupBy(
        "source_financial_year",
        "Line_Name"
    )
    .agg(
        sum("Passenger_Boardings").alias("total_boardings"),
        sum("Passenger_Alightings").alias("total_alightings")
    )
)

# ---------------------------------------------------------------------
# GOLD_CAPACITY_UTILISATION
# ---------------------------------------------------------------------

gold_capacity_utilisation = (
    fact_df
    .groupBy("Line_Name")
    .agg(
        avg("Passenger_Arrival_Load").alias(
            "avg_arrival_load"
        ),
        avg("Passenger_Departure_Load").alias(
            "avg_departure_load"
        ),
        max("Passenger_Departure_Load").alias(
            "peak_departure_load"
        )
    )
)

# ---------------------------------------------------------------------
# GOLD_FORECAST_INPUT
# ---------------------------------------------------------------------

gold_forecast_input = (
    fact_df
    .groupBy(
        date_format("Business_Date", "yyyy-MM").alias("year_month")
    )
    .agg(
        sum("Passenger_Boardings").alias(
            "total_boardings"
        )
    )
    .orderBy("year_month")
)

# ---------------------------------------------------------------------
# Write Gold Tables
# ---------------------------------------------------------------------

gold_passenger_demand.write.mode(
    "overwrite"
).parquet(
    "data/gold/gold_passenger_demand"
)

gold_station_demand.write.mode(
    "overwrite"
).parquet(
    "data/gold/gold_station_demand"
)

gold_line_growth.write.mode(
    "overwrite"
).parquet(
    "data/gold/gold_line_growth"
)

gold_capacity_utilisation.write.mode(
    "overwrite"
).parquet(
    "data/gold/gold_capacity_utilisation"
)

gold_forecast_input.write.mode(
    "overwrite"
).parquet(
    "data/gold/gold_forecast_input"
)

# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

print("\n==============================")
print("GOLD SUMMARY")
print("==============================")

print(
    f"GOLD_PASSENGER_DEMAND: "
    f"{gold_passenger_demand.count():,}"
)

print(
    f"GOLD_STATION_DEMAND: "
    f"{gold_station_demand.count():,}"
)

print(
    f"GOLD_LINE_GROWTH: "
    f"{gold_line_growth.count():,}"
)

print(
    f"GOLD_CAPACITY_UTILISATION: "
    f"{gold_capacity_utilisation.count():,}"
)

print(
    f"GOLD_FORECAST_INPUT: "
    f"{gold_forecast_input.count():,}"
)

spark.stop()

print("\nGold layer created successfully.")