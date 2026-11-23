
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

# Load datasets
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")
shipments = pd.read_csv(DATA_DIR / "shipments.csv")

# Join purchase orders, suppliers and shipments
data = purchase_orders.merge(
    suppliers.drop(columns=["status"]),
    on="supplier_id",
    how="left"
).merge(
    shipments,
    on="order_id",
    how="left"
)

# Convert date columns
data["expected_date"] = pd.to_datetime(
    data["expected_date"], errors="coerce"
)

data["delivery_date"] = pd.to_datetime(
    data["delivery_date"], errors="coerce"
)

data["dispatch_date"] = pd.to_datetime(
    data["dispatch_date"], errors="coerce"
)

# Consider only delivered orders with actual delivery dates
delivered = data[
    (data["status"] == "Delivered") &
    (data["delivery_date"].notna()) &
    (data["expected_date"].notna())
].copy()

# Calculate delivery delay
delivered["delay_days"] = (
    delivered["delivery_date"] -
    delivered["expected_date"]
).dt.days

delivered["on_time"] = delivered["delay_days"] <= 0

# Calculate actual shipment transit time
delivered["transit_days"] = (
    delivered["delivery_date"] -
    delivered["dispatch_date"]
).dt.days

# Supplier-wise performance
performance = []

for supplier_id, supplier_data in data.groupby("supplier_id"):

    delivered_data = delivered[
        delivered["supplier_id"] == supplier_id
    ]

    total_orders = len(supplier_data)
    delivered_count = len(delivered_data)

    on_time_count = (
        delivered_data["on_time"].sum()
        if delivered_count > 0 else 0
    )

    on_time_rate = (
        (on_time_count / delivered_count) * 100
        if delivered_count > 0 else 0
    )

    delayed_count = (
        supplier_data["status"] == "Delayed"
    ).sum()

    average_transit = (
        delivered_data["transit_days"].mean()
        if delivered_count > 0 else None
    )

    # Risk flags
    if delayed_count >= 2 or (
        delivered_count > 0 and on_time_rate < 80
    ):
        risk = "High"
    elif delayed_count == 1:
        risk = "Medium"
    else:
        risk = "Normal"

    performance.append({
        "supplier_id": supplier_id,
        "supplier_name": supplier_data["supplier_name"].iloc[0],
        "total_orders": total_orders,
        "delivered_orders": delivered_count,
        "on_time_deliveries": int(on_time_count),
        "on_time_delivery_rate": round(on_time_rate, 2),
        "delayed_orders": int(delayed_count),
        "average_transit_days": (
            round(average_transit, 2)
            if pd.notna(average_transit) else None
        ),
        "risk_level": risk
    })

supplier_report = pd.DataFrame(performance)

# Save report
REPORT_DIR.mkdir(exist_ok=True)

supplier_report.to_csv(
    REPORT_DIR / "supplier_performance.csv",
    index=False
)

print("Suppliers analyzed:", len(supplier_report))
print("\nSupplier Performance:")
print(supplier_report.to_string(index=False))

print("\nSupplier performance analysis completed!")
