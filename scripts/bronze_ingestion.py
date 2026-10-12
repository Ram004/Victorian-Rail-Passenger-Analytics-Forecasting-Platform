from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from functools import reduce

# -----------------------------------------------------------------------------
# Create Spark Session
# -----------------------------------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Metro Bronze Ingestion")
    .config("spark.driver.memory", "16g")
    .config("spark.executor.memory", "16g")
    .getOrCreate()
)

# -----------------------------------------------------------------------------
# Source Files
# -----------------------------------------------------------------------------

files = {
    "2018-19": "data/raw/train_service_passenger_counts_fy_2018_2019.csv",
    "2019-20": "data/raw/train_service_passenger_counts_fy_2019_2020.csv",
    "2020-21": "data/raw/train_service_passenger_counts_fy_2020_2021.csv",
    "2021-22": "data/raw/train_service_passenger_counts_fy_2021_2022.csv",
    "2022-23": "data/raw/train_service_passenger_counts_fy_2022_2023.csv",
    "2023-24": "data/raw/train_service_passenger_counts_fy_2023_2024.csv",
    "2024-25": "data/raw/train_service_passenger_counts_fy_2024_2025.csv"
}

# -----------------------------------------------------------------------------
# Read Files
# -----------------------------------------------------------------------------

dataframes = []

for fy, file_path in files.items():

    print(f"\nReading {fy}...")

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(file_path)
    )

    df = df.withColumn("source_financial_year", lit(fy))

    print(f"{fy} Rows: {df.count():,}")

    dataframes.append(df)

# -----------------------------------------------------------------------------
# Merge All Years
# -----------------------------------------------------------------------------

print("\nMerging datasets...")

bronze_df = reduce(lambda df1, df2: df1.unionByName(df2), dataframes)

# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

total_rows = bronze_df.count()

print("\n========================================")
print("BRONZE DATASET SUMMARY")
print("========================================")
print(f"Total Rows: {total_rows:,}")
print(f"Total Columns: {len(bronze_df.columns)}")
print("========================================")

# -----------------------------------------------------------------------------
# Write Bronze Layer
# -----------------------------------------------------------------------------

output_path = "data/bronze/bronze_passenger_counts"

print("\nWriting Bronze layer...")

(
    bronze_df.write
    .mode("overwrite")
    .parquet(output_path)
)

print(f"\nBronze layer written to:")
print(output_path)

# -----------------------------------------------------------------------------
# Stop Spark
# -----------------------------------------------------------------------------

spark.stop()

print("\nBronze ingestion completed successfully.")