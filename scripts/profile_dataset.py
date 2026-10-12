from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when, min, max

# Create Spark Session
spark = SparkSession.builder \
    .appName("Metro Profiling") \
    .config("spark.driver.memory", "16g") \
    .config("spark.executor.memory", "16g") \
    .getOrCreate()


print("Driver Memory:",
      spark.sparkContext.getConf().get("spark.driver.memory"))

print("Executor Memory:",
      spark.sparkContext.getConf().get("spark.executor.memory"))

# Read Data
df = spark.read.csv(
    "data/raw/train_service_passenger_counts_fy_2024_2025.csv",
    header=True,
    inferSchema=True
)

# Schema
print("\n========== SCHEMA ==========")
df.printSchema()

# Row Count
print("\n========== ROW COUNT ==========")
print(f"Rows: {df.count():,}")

# Distinct Counts
print("\n========== CARDINALITY ==========")

print(f"Distinct Lines: {df.select('Line_Name').distinct().count():,}")
print(f"Distinct Stations: {df.select('Station_Name').distinct().count():,}")
print(f"Distinct Train Services: {df.select('Train_Number').distinct().count():,}")

# Date Range
print("\n========== DATE RANGE ==========")

df.select(
    min("Business_Date").alias("Min_Date"),
    max("Business_Date").alias("Max_Date")
).show(truncate=False)

# Null Analysis
print("\n========== NULL COUNTS ==========")

null_counts = df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
])

null_counts.show(vertical=True, truncate=False)

# Duplicate Analysis
print("\n========== DUPLICATE CHECK ==========")

duplicate_count = (
    df.groupBy(
        "Business_Date",
        "Train_Number",
        "Station_Name",
        "Stop_Sequence_Number"
    )
    .count()
    .filter("count > 1")
    .count()
)

print(f"Duplicate Records: {duplicate_count:,}")

# Sample Data
print("\n========== SAMPLE DATA ==========")

df.show(5, truncate=False)

print("\n========== PROFILING COMPLETE ==========")

spark.stop()