
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

# Load datasets
sales = pd.read_csv(DATA_DIR / "sales.csv")
inventory = pd.read_csv(DATA_DIR / "inventory.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")

# Calculate average daily demand
daily_demand = (
    sales.groupby("product_id")["quantity_sold"]
    .mean()
    .reset_index(name="average_daily_demand")
)

# Calculate open purchase order quantities
open_orders = purchase_orders[
    purchase_orders["status"].isin(
        ["Pending", "In Transit", "Delayed"]
    )
]

open_quantity = (
    open_orders.groupby("product_id")["quantity"]
    .sum()
    .reset_index(name="open_order_quantity")
)

# Calculate average supplier lead time
default_lead_time = suppliers["lead_time"].mean()

# Get product-specific supplier lead times
product_lead_times = (
    purchase_orders.merge(
        suppliers[["supplier_id", "lead_time"]],
        on="supplier_id",
        how="left"
    )
    .groupby("product_id")["lead_time"]
    .mean()
    .reset_index()
)

# Combine inventory information
analysis = (
    inventory.merge(products, on="product_id", how="left")
    .merge(daily_demand, on="product_id", how="left")
    .merge(open_quantity, on="product_id", how="left")
    .merge(product_lead_times, on="product_id", how="left")
)

analysis["average_daily_demand"] = (
    analysis["average_daily_demand"].fillna(0)
)

analysis["open_order_quantity"] = (
    analysis["open_order_quantity"].fillna(0)
)

analysis["lead_time"] = (
    analysis["lead_time"].fillna(default_lead_time)
)

# Inventory calculations
analysis["safety_stock"] = (
    analysis["average_daily_demand"] * 2
)

analysis["reorder_point"] = (
    analysis["average_daily_demand"]
    * (analysis["lead_time"] + 2)
)

analysis["inventory_position"] = (
    analysis["quantity_available"]
    + analysis["open_order_quantity"]
)

# Identify inventory risk
def get_risk(row):
    if row["inventory_position"] <= (
        row["average_daily_demand"] * row["lead_time"]
    ):
        return "Critical"

    elif row["inventory_position"] <= row["reorder_point"]:
        return "High"

    return "Normal"

analysis["risk_level"] = analysis.apply(get_risk, axis=1)

# Suggested replenishment for 14 days of demand
analysis["suggested_replenishment"] = (
    analysis["average_daily_demand"] * 14
    - analysis["inventory_position"]
).clip(lower=0).apply(lambda value: round(value))

# Save report
REPORT_DIR.mkdir(exist_ok=True)

analysis.to_csv(
    REPORT_DIR / "inventory_risk_analysis.csv",
    index=False
)

print("Products analyzed:", len(analysis))
print("\nInventory Risk Summary:")
print(analysis["risk_level"].value_counts())

print("\nProducts requiring replenishment:")
print(
    analysis.loc[
        analysis["suggested_replenishment"] > 0,
        ["product_id", "risk_level", "suggested_replenishment"]
    ].to_string(index=False)
)

print("\nInventory optimization completed successfully!")
