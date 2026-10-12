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

print(
    "Distinct Lines:",
    bronze_df.select("Line_Name").distinct().count()
)

print(
    "Distinct Stations:",
    bronze_df.select("Station_Name").distinct().count()
)

print(
    "Distinct Train Numbers:",
    bronze_df.select("Train_Number").distinct().count()
)

print(
    "Distinct Train Services:",
    bronze_df.select(
        "Train_Number",
        "Origin_Station",
        "Destination_Station"
    ).distinct().count()
)

spark.stop()