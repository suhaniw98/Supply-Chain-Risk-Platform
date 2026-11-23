
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

sales = pd.read_csv(DATA_DIR / "sales.csv")
sales["sale_date"] = pd.to_datetime(sales["sale_date"])

# Product-wise sales
product_sales = (
    sales.groupby("product_id")["quantity_sold"]
    .sum()
    .reset_index(name="total_sales")
)

# Daily average demand
daily_demand = (
    sales.groupby("product_id")["quantity_sold"]
    .mean()
    .reset_index(name="average_daily_demand")
)

# Monthly sales trend
sales["month"] = sales["sale_date"].dt.to_period("M").astype(str)

monthly_sales = (
    sales.groupby("month")["quantity_sold"]
    .sum()
    .reset_index()
)

# Highest demand product
highest_product = product_sales.loc[
    product_sales["total_sales"].idxmax()
]

# Save reports
product_sales.to_csv(
    REPORT_DIR / "product_sales_summary.csv", index=False
)

daily_demand.to_csv(
    REPORT_DIR / "daily_demand_summary.csv", index=False
)

monthly_sales.to_csv(
    REPORT_DIR / "monthly_sales_trend.csv", index=False
)

# Plot monthly sales
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales["month"],
    monthly_sales["quantity_sold"],
    marker="o"
)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(REPORT_DIR / "monthly_sales_trend.png")
plt.close()

print("Total sales records:", len(sales))
print("Products analyzed:", sales["product_id"].nunique())
print("Highest demand product:", highest_product["product_id"])
print("Total units sold:", sales["quantity_sold"].sum())
print("\nDemand analysis completed successfully!")
