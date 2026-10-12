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

tables = {
    "GOLD_PASSENGER_DEMAND":
        "data/gold/gold_passenger_demand",

    "GOLD_STATION_DEMAND":
        "data/gold/gold_station_demand",

    "GOLD_LINE_GROWTH":
        "data/gold/gold_line_growth",

    "GOLD_CAPACITY_UTILISATION":
        "data/gold/gold_capacity_utilisation",

    "GOLD_FORECAST_INPUT":
        "data/gold/gold_forecast_input"
}

for table_name, path in tables.items():

    print(f"Loading {table_name}")

    df = pd.read_parquet(path)

    print("Original Columns:")
    print(df.columns.tolist())

    df.columns = [c.upper() for c in df.columns]

    print("Snowflake Columns:")
    print(df.columns.tolist())

    success, chunks, rows, _ = write_pandas(
        conn,
        df,
        table_name,
        auto_create_table=False
    )

    print(
        f"Success: {success} "
        f"Rows Loaded: {rows:,}"
    )

conn.close()
