from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Silver Validation")
    .config("spark.driver.memory", "16g")
    .getOrCreate()
)

bronze_df = spark.read.parquet(
    "data/bronze/bronze_passenger_counts"
)

print("\n==============================")
print("DIMENSION VALIDATION")
print("==============================")

line_count = bronze_df.select("Line_Name").distinct().count()
station_count = bronze_df.select("Station_Name").distinct().count()
train_count = bronze_df.select("Train_Number").distinct().count()

train_service_count = (
    bronze_df.select(
        "Train_Number",
        "Origin_Station",
        "Destination_Station"
    )
    .distinct()
    .count()
)

print(f"Distinct Line Names: {line_count:,}")
print(f"Distinct Station Names: {station_count:,}")
print(f"Distinct Train Numbers: {train_count:,}")
print(f"Distinct Train Service Combinations: {train_service_count:,}")

print("\n==============================")
print("LINE NAME / GROUP / MODE")
print("==============================")

bronze_df.select(
    "Line_Name",
    "Group",
    "Mode"
).distinct().orderBy(
    "Line_Name"
).show(100, False)

print("\n==============================")
print("DIRECTIONS")
print("==============================")

bronze_df.select(
    "Direction"
).distinct().show(False)

spark.stop()