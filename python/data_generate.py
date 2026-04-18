import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

# -----------------------------
# SETUP
# -----------------------------
fake = Faker()
random.seed(42)
np.random.seed(42)

TODAY = datetime.today()

# -----------------------------
# 1. PRODUCTS TABLE
# -----------------------------
categories = ["Antibiotic", "Painkiller", "Vitamin", "Syrup", "Skin Care"]

products = []
for pid in range(1, 51):
    mrp = random.randint(60, 500)
    cost_price = round(mrp * random.uniform(0.55, 0.75), 2)

    products.append([
        pid,
        f"Medicine_{pid}",
        random.choice(categories),
        mrp,
        cost_price
    ])

products_df = pd.DataFrame(
    products,
    columns=["product_id", "medicine_name", "category", "mrp", "cost_price"]
)

# -----------------------------
# 2. INVENTORY BATCHES
# -----------------------------
batches = []
batch_id = 1

for _, product in products_df.iterrows():
    for _ in range(random.randint(1, 3)):
        expiry_date = fake.date_between(start_date="-6m", end_date="+12m")
        quantity_received = random.randint(50, 300)

        batches.append([
            batch_id,
            product["product_id"],
            expiry_date,
            quantity_received
        ])
        batch_id += 1

batches_df = pd.DataFrame(
    batches,
    columns=["batch_id", "product_id", "expiry_date", "quantity_received"]
)

# -----------------------------
# 3. SALES (WITH LEAKAGE)
# -----------------------------
sales = []
sale_id = 1

for _, batch in batches_df.iterrows():
    sales_count = random.randint(8, 20)

    product = products_df[
        products_df["product_id"] == batch["product_id"]
    ].iloc[0]

    for _ in range(sales_count):
        sale_date = fake.date_between(start_date="-5m", end_date="today")
        quantity_sold = random.randint(1, 5)

        # Intentional pricing leakage
        selling_price = round(
            product["mrp"] * random.uniform(0.7, 1.25), 2
        )

        sales.append([
            sale_id,
            batch["product_id"],
            batch["batch_id"],
            sale_date,
            quantity_sold,
            selling_price
        ])
        sale_id += 1

sales_df = pd.DataFrame(
    sales,
    columns=[
        "sale_id",
        "product_id",
        "batch_id",
        "sale_date",
        "quantity_sold",
        "selling_price"
    ]
)

# -----------------------------
# 4. RETURNS (LEAKAGE SCENARIOS)
# -----------------------------
returns = []

sample_sales = sales_df.sample(frac=0.18, random_state=42)

for _, sale in sample_sales.iterrows():
    quantity_returned = random.choice([0, 1])

    if quantity_returned > 0:
        returns.append([
            sale["sale_id"],
            fake.date_between(start_date=sale["sale_date"], end_date="today"),
            quantity_returned
        ])

returns_df = pd.DataFrame(
    returns,
    columns=["sale_id", "return_date", "quantity_returned"]
)

# -----------------------------
# EXPORT CSV FILES
# -----------------------------
products_df.to_csv("data/products.csv", index=False)
batches_df.to_csv("data/inventory_batches.csv", index=False)
sales_df.to_csv("data/sales.csv", index=False)
returns_df.to_csv("data/returns.csv", index=False)

print("✅ Medical store revenue leakage data generated successfully.")