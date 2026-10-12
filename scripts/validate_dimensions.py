from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Dimension Validation")
    .config("spark.driver.memory", "16g")
    .getOrCreate()
)

bronze_df = spark.read.parquet(
    "data/bronze/bronze_passenger_counts"
)

print(
    "\nDistinct Line Names:",
    bronze_df.select("Line_Name")
    .distinct()
    .count()
)

print(
    "Distinct Station Names:",
    bronze_df.select("Station_Name")
    .distinct()
    .count()
)

print(
    "Distinct Train Numbers:",
    bronze_df.select("Train_Number")
    .distinct()
    .count()
)

print(
    "Distinct Train Service Combinations:",
    bronze_df.select(
        "Train_Number",
        "Origin_Station",
        "Destination_Station"
    )
    .distinct()
    .count()
)

spark.stop()