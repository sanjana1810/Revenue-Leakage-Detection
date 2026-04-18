import sqlite3
import pandas as pd

conn = sqlite3.connect("medical_leakage.db")

# 1 Total Revenue
query_revenue = """
SELECT SUM(quantity_sold * selling_price) AS total_revenue
FROM sales
"""
revenue = pd.read_sql(query_revenue, conn)
print("\nTotal Revenue")
print(revenue)

# 2 Expired Medicine Sold
query_expired = """
SELECT COUNT(*) AS expired_sales
FROM sales s
JOIN inventory_batches b
ON s.batch_id = b.batch_id
WHERE s.sale_date > b.expiry_date
"""
expired = pd.read_sql(query_expired, conn)
print("\nExpired Medicines Sold")
print(expired)

# 3 MRP Violation
query_mrp = """
SELECT COUNT(*) AS mrp_violations
FROM sales s
JOIN products p
ON s.product_id = p.product_id
WHERE s.selling_price > p.mrp
"""
mrp = pd.read_sql(query_mrp, conn)
print("\nMRP Violations")
print(mrp)

# 4 Revenue Leakage Amount
query_leakage = """
SELECT SUM((p.mrp - s.selling_price) * s.quantity_sold) AS leakage_amount
FROM sales s
JOIN products p
ON s.product_id = p.product_id
WHERE s.selling_price < p.mrp
"""
leakage = pd.read_sql(query_leakage, conn)
print("\nRevenue Leakage")
print(leakage)

# 5 Top 10 Medicines With Leakage
query_top_leak = """
SELECT p.medicine_name,
SUM((p.mrp - s.selling_price) * s.quantity_sold) AS leakage_amount
FROM sales s
JOIN products p
ON s.product_id = p.product_id
WHERE s.selling_price < p.mrp
GROUP BY p.medicine_name
ORDER BY leakage_amount DESC
LIMIT 10
"""
top_leak = pd.read_sql(query_top_leak, conn)
print("\nTop Leakage Medicines")
print(top_leak)

conn.close()