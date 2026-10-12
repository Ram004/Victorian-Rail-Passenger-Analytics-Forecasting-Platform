from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id

# --------------------------------------------------------------------
# Spark Session
# --------------------------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Metro Silver Transformations")
    .config("spark.driver.memory", "16g")
    .config("spark.executor.memory", "16g")
    .getOrCreate()
)

# --------------------------------------------------------------------
# Read Bronze
# --------------------------------------------------------------------

bronze_df = spark.read.parquet(
    "data/bronze/bronze_passenger_counts"
)

print(f"Bronze Rows: {bronze_df.count():,}")

# --------------------------------------------------------------------
# DIM_DATE
# --------------------------------------------------------------------

dim_date = (
    bronze_df
    .select(
        "Business_Date",
        "Day_of_Week",
        "Day_Type"
    )
    .distinct()
    .withColumn("date_key", monotonically_increasing_id())
)

# --------------------------------------------------------------------
# DIM_LINE
# --------------------------------------------------------------------

dim_line = (
    bronze_df
    .select(
        "Line_Name"
    )
    .distinct()
    .withColumn("line_key", monotonically_increasing_id())
)

# --------------------------------------------------------------------
# DIM_STATION
# --------------------------------------------------------------------

dim_station = (
    bronze_df
    .select(
        "Station_Name",
        "Station_Latitude",
        "Station_Longitude",
        "Station_Chainage"
    )
    .distinct()
    .withColumn("station_key", monotonically_increasing_id())
)

# --------------------------------------------------------------------
# DIM_DIRECTION
# --------------------------------------------------------------------

dim_direction = (
    bronze_df
    .select(
        "Direction"
    )
    .distinct()
    .withColumn("direction_key", monotonically_increasing_id())
)

# --------------------------------------------------------------------
# DIM_TRAIN_SERVICE
# --------------------------------------------------------------------

dim_train_service = (
    bronze_df
    .select(
        "Train_Number",
        "Origin_Station",
        "Destination_Station"
    )
    .distinct()
    .withColumn("train_service_key", monotonically_increasing_id())
)

# --------------------------------------------------------------------
# FACT_PASSENGER_COUNTS
# --------------------------------------------------------------------

fact_passenger_counts = (
    bronze_df
    .select(
        "Business_Date",
        "Train_Number",
        "Line_Name",
        "Station_Name",
        "Direction",
        "Passenger_Boardings",
        "Passenger_Alightings",
        "Passenger_Arrival_Load",
        "Passenger_Departure_Load",
        "source_financial_year"
    )
)

# --------------------------------------------------------------------
# Write Silver Dimensions
# --------------------------------------------------------------------

dim_date.write.mode("overwrite").parquet(
    "data/silver/dim_date"
)

dim_line.write.mode("overwrite").parquet(
    "data/silver/dim_line"
)

dim_station.write.mode("overwrite").parquet(
    "data/silver/dim_station"
)

dim_direction.write.mode("overwrite").parquet(
    "data/silver/dim_direction"
)

dim_train_service.write.mode("overwrite").parquet(
    "data/silver/dim_train_service"
)

fact_passenger_counts.write.mode("overwrite").parquet(
    "data/silver/fact_passenger_counts"
)

# --------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------

print("\nSILVER SUMMARY")
print(f"DIM_DATE: {dim_date.count():,}")
print(f"DIM_LINE: {dim_line.count():,}")
print(f"DIM_STATION: {dim_station.count():,}")
print(f"DIM_DIRECTION: {dim_direction.count():,}")
print(f"DIM_TRAIN_SERVICE: {dim_train_service.count():,}")
print(f"FACT_PASSENGER_COUNTS: {fact_passenger_counts.count():,}")

spark.stop()

print("\nSilver layer created successfully.")