
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

# Load cleaned datasets
products = pd.read_csv(DATA_DIR / "products.csv")
sales = pd.read_csv(DATA_DIR / "sales.csv")
inventory = pd.read_csv(DATA_DIR / "inventory.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")
shipments = pd.read_csv(DATA_DIR / "shipments.csv")

# Join sales with products
sales_analysis = sales.merge(
    products,
    on="product_id",
    how="left"
)

# Join inventory with products
inventory_analysis = inventory.merge(
    products,
    on="product_id",
    how="left"
)

# Join purchase orders with products and suppliers
purchase_analysis = purchase_orders.merge(
    products,
    on="product_id",
    how="left"
).merge(
    suppliers,
    on="supplier_id",
    how="left"
)

# Join purchase orders with shipment details
shipment_analysis = purchase_analysis.merge(
    shipments,
    on="order_id",
    how="left"
)

# Save integrated datasets
REPORT_DIR.mkdir(exist_ok=True)

sales_analysis.to_csv(
    REPORT_DIR / "sales_analysis.csv", index=False
)

inventory_analysis.to_csv(
    REPORT_DIR / "inventory_analysis.csv", index=False
)

purchase_analysis.to_csv(
    REPORT_DIR / "purchase_analysis.csv", index=False
)

shipment_analysis.to_csv(
    REPORT_DIR / "shipment_analysis.csv", index=False
)

print("Sales records:", len(sales_analysis))
print("Inventory records:", len(inventory_analysis))
print("Purchase order records:", len(purchase_analysis))
print("Shipment analysis records:", len(shipment_analysis))

print("\nData integration completed successfully!")
