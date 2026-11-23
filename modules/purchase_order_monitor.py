
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

# Load datasets
orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")
shipments = pd.read_csv(DATA_DIR / "shipments.csv")
inventory_risk = pd.read_csv(
    REPORT_DIR / "inventory_risk_analysis.csv"
)

# Convert dates
orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

orders["expected_date"] = pd.to_datetime(
    orders["expected_date"], errors="coerce"
)

shipments["dispatch_date"] = pd.to_datetime(
    shipments["dispatch_date"], errors="coerce"
)

shipments["delivery_date"] = pd.to_datetime(
    shipments["delivery_date"], errors="coerce"
)

# Join order and shipment information
monitor = orders.merge(
    shipments,
    on="order_id",
    how="left"
)

# Calculate overdue status
today = pd.Timestamp.today().normalize()

open_statuses = ["Pending", "In Transit", "Delayed"]

monitor["is_overdue"] = (
    monitor["status"].isin(open_statuses)
    & (monitor["expected_date"] < today)
)

monitor["days_overdue"] = (
    today - monitor["expected_date"]
).dt.days

monitor.loc[
    ~monitor["is_overdue"], "days_overdue"
] = 0

# Identify affected products
monitor = monitor.merge(
    inventory_risk[
        [
            "product_id",
            "quantity_available",
            "risk_level",
            "suggested_replenishment"
        ]
    ],
    on="product_id",
    how="left"
)

# Create monitoring alerts
def get_alert(row):
    if row["is_overdue"]:
        return "Overdue Shipment"

    if row["risk_level"] == "Critical":
        return "Critical Inventory Risk"

    if row["status"] == "Delayed":
        return "Delayed Order"

    return "Normal"

monitor["alert"] = monitor.apply(get_alert, axis=1)

# Calculate fulfillment rate
total_orders = len(monitor)
delivered_orders = (monitor["status"] == "Delivered").sum()

fulfillment_rate = (
    delivered_orders / total_orders * 100
    if total_orders > 0 else 0
)

# Save report
REPORT_DIR.mkdir(exist_ok=True)

monitor.to_csv(
    REPORT_DIR / "purchase_order_monitoring.csv",
    index=False
)

print("Total purchase orders:", total_orders)
print("Delivered orders:", delivered_orders)
print("Fulfillment rate:", round(fulfillment_rate, 2), "%")
print("Overdue orders:", int(monitor["is_overdue"].sum()))

print("\nPurchase Order Alerts:")
print(
    monitor[
        ["order_id", "product_id", "status",
         "is_overdue", "days_overdue", "alert"]
    ].to_string(index=False)
)

print("\nPurchase order monitoring completed successfully!")
