import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# === Config ===
CSV_FILE = input("Enter CSV file path: ").strip()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

SCHEMA_NAME = "floatchat"
tableName = os.getenv("TABLE_NAME")
TABLE_NAME = f"{SCHEMA_NAME}.{tableName}"
BATCH_SIZE = 1000
CHUNK_SIZE = 10000  # Number of rows per chunk from CSV

# === Connect to PostgreSQL ===
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# === Create schema and table (idempotent) ===
cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME};")
cur.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    time TIMESTAMP,
    latitude NUMERIC(10,4),
    longitude NUMERIC(10,4),
    depth NUMERIC(10,4),
    temperature NUMERIC(10,4),
    salinity NUMERIC(10,4)
);
""")
conn.commit()

# === Process CSV in chunks ===
rows_batch = []

try:
    for chunk in tqdm(pd.read_csv(CSV_FILE, parse_dates=["time"], chunksize=CHUNK_SIZE), desc="Processing CSV",
                      unit="chunk"):
        # Ensure required columns exist
        required_cols = {"time", "latitude", "longitude", "depth", "temperature", "salinity"}
        if not required_cols.issubset(chunk.columns):
            raise ValueError(f"Missing columns. Found: {list(chunk.columns)}")

        # Round numeric values
        for col in ["latitude", "longitude", "depth", "temperature", "salinity"]:
            chunk[col] = chunk[col].round(4)

        # Add rows to batch
        for row in chunk.itertuples(index=False):
            rows_batch.append((
                row.time.to_pydatetime() if pd.notnull(row.time) else None,
                row.latitude,
                row.longitude,
                row.depth,
                row.temperature,
                row.salinity
            ))

            # Insert batch if full
            if len(rows_batch) >= BATCH_SIZE:
                try:
                    cur.executemany(f"""
                        INSERT INTO {TABLE_NAME} (time, latitude, longitude, depth, temperature, salinity)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, rows_batch)
                    conn.commit()
                    rows_batch = []
                except Exception as batch_err:
                    conn.rollback()
                    tqdm.write(f"⚠️ Batch insert failed: {batch_err}")

except Exception as e:
    print(f"❌ Error processing CSV: {e}")

# Insert remaining rows
if rows_batch:
    try:
        cur.executemany(f"""
            INSERT INTO {TABLE_NAME} (time, latitude, longitude, depth, temperature, salinity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, rows_batch)
        conn.commit()
    except Exception as final_err:
        conn.rollback()
        print(f"⚠️ Final batch insert failed: {final_err}")

print(f"\n🎉 Finished! Data inserted into PostgreSQL table `{TABLE_NAME}`")

query = f"SELECT * FROM {TABLE_NAME} LIMIT 5;"
df = pd.read_sql(query, conn)

print("\n📊 First 5 rows:")
print(df)

query_count = f"SELECT COUNT(*) FROM {TABLE_NAME};"
total_rows = pd.read_sql(query_count, conn).iloc[0, 0]
print(f"\n✅ Total rows in table: {total_rows}")

# Close cursor and connection
cur.close()
conn.close()
