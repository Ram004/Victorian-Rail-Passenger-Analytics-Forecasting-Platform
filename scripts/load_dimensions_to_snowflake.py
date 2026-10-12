from dotenv import load_dotenv
import os

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

print("Connected to Snowflake")

tables = {
    "DIM_DATE": "data/silver/dim_date",
    "DIM_LINE": "data/silver/dim_line",
    "DIM_STATION": "data/silver/dim_station",
    "DIM_DIRECTION": "data/silver/dim_direction",
    "DIM_TRAIN_SERVICE": "data/silver/dim_train_service"
}

for table_name, path in tables.items():

    print(f"\nLoading {table_name}")

    df = pd.read_parquet(path)

    # Convert columns to Snowflake naming convention
    df.columns = [c.upper() for c in df.columns]

    success, chunks, rows, _ = write_pandas(
        conn,
        df,
        table_name,
        auto_create_table=False
    )

    print(f"Success: {success}")
    print(f"Rows Loaded: {rows:,}")

conn.close()

print("\nDimension load completed successfully.")