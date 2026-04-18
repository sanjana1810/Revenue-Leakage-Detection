import sqlite3
import pandas as pd

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("medical_leakage.db")

# Load CSV files
products = pd.read_csv("data/products.csv")
batches = pd.read_csv("data/inventory_batches.csv")
sales = pd.read_csv("data/sales.csv")
returns = pd.read_csv("data/returns.csv")

# Write tables into SQLite
products.to_sql("products", conn, if_exists="replace", index=False)
batches.to_sql("inventory_batches", conn, if_exists="replace", index=False)
sales.to_sql("sales", conn, if_exists="replace", index=False)
returns.to_sql("returns", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("✅ Data successfully loaded into SQLite database")