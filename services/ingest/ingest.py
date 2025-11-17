import os
import shutil
import glob
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Environment variables (provide sensible defaults)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "staging_db")
RAW_DATA = os.getenv("RAW_DATA", "/data/raw")
INGESTED_DATA = os.getenv("INGESTED_DATA", "/data/ingested")

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Find all CSV files in RAW_DATA
pattern = os.path.join(RAW_DATA, "*.csv")
files = sorted(glob.glob(pattern))

if not files:
    print(f"No CSV files found in {RAW_DATA}. Exiting.")
else:
    total_rows = 0
    processed_files = 0

    for file_path in files:
        filename = os.path.basename(file_path)
        try:
            # Ingest the file
            print(f"Reading file: {file_path}")
            df = pd.read_csv(file_path)
            ingest_ts = pd.Timestamp.utcnow()
            df["ingested_at"] = ingest_ts
            df.to_sql("customers", engine, if_exists="append", index=False)

            rows = len(df)
            total_rows += rows
            processed_files += 1
            print(f"Appended {rows} rows from {filename} to Postgres table 'customers'.")

            # Move the file to ingested folder
            dest_path = os.path.join(INGESTED_DATA, filename)
            shutil.move(file_path, dest_path)
            print(f"Moved {file_path} -> {dest_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            raise

    print(f"Ingestion complete. Processed files: {processed_files}. Total rows appended: {total_rows}.")
