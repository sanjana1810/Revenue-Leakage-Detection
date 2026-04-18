import sqlite3
import pandas as pd

conn = sqlite3.connect("medical_leakage.db")

query = "SELECT COUNT(*) as total_sales FROM sales"

df = pd.read_sql(query, conn)

print(df)

conn.close()