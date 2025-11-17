import streamlit as st
import pandas as pd
import duckdb
import os

DUCKDB_PATH = os.getenv("DUCKDB_PATH")

# Connect to DuckDB
con = duckdb.connect(DUCKDB_PATH)
df = con.execute("SELECT * FROM customers").df()
con.close()

st.title("Customer Churn Dashboard")


st.write("Total rows:", len(df))
st.write("Showing first 5 rows")
st.dataframe(df.head())

# counts for Gender
gender_counts = df['Gender'].value_counts()
st.subheader("Gender counts")
st.table(gender_counts.rename_axis('Gender').reset_index(name='count'))

# Revenu

total_charges_sum = df['TotalCharges'].sum()
st.subheader("Total Charges sum")
st.write(f"{total_charges_sum:,.2f} EUR")
