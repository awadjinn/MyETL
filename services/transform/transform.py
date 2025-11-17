import os
import pandas as pd
import duckdb
from sqlalchemy import create_engine
import hashlib


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DUCKDB_PATH = os.getenv("DUCKDB_PATH")

engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Load data
df = pd.read_sql("SELECT * FROM customers", engine)
df.sort_values("ingested_at", ascending=False, inplace=True)
df.drop_duplicates(subset=["CustomerID"], keep="first", inplace=True)

print(f"After dedup: {df['CustomerID'].nunique()} unique CustomerID, total rows {len(df)}")

# Handle missing values
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Gender'] = df['Gender'].fillna("Unknown")
df['Tenure'] = df['Tenure'].fillna(0)
df['MonthlyCharges'] = df['MonthlyCharges'].fillna(0.0)
df['ContractType'] = df['ContractType'].fillna("Unknown")
df['InternetService'] = df['InternetService'].fillna("Unknown")
df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
df['TechSupport'] = df['TechSupport'].fillna("No")
df['Churn'] = df['Churn'].fillna("No")

# Anonymize PII
# Since there no PII in the dataset, I've wrote an example
# df['CustomerName'] = df['CustomerName'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

# Write to DuckDB 
con = duckdb.connect(DUCKDB_PATH)
con.register('df_view', df)
con.execute("DROP TABLE IF EXISTS customers")
con.execute("CREATE TABLE customers AS SELECT * FROM df_view")
# optional: unregister the view
try:
    con.unregister('df_view')
except Exception:
    pass
con.close()

print(f"Loaded customers: {len(df)} rows")
