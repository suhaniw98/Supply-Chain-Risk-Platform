
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLEAN_DIR = DATA_DIR / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

CLEAN_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# Load datasets
products = pd.read_csv(DATA_DIR / "products.csv")
sales = pd.read_csv(DATA_DIR / "sales.csv")
inventory = pd.read_csv(DATA_DIR / "inventory.csv")
suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
purchase_orders = pd.read_csv(DATA_DIR / "purchase_orders.csv")
shipments = pd.read_csv(DATA_DIR / "shipments.csv")

quality_logs = []
rejected_records = []

def log_issue(dataset, issue, count):
    quality_logs.append({
        "dataset": dataset,
        "issue": issue,
        "record_count": count
    })

def check_duplicates(df, dataset, column):
    duplicate_count = df[column].duplicated().sum()
    log_issue(dataset, "Duplicate " + column, duplicate_count)
    return df.drop_duplicates(subset=column).copy()

# Check duplicate records
products = check_duplicates(products, "products", "product_id")
suppliers = check_duplicates(suppliers, "suppliers", "supplier_id")
sales = sales.drop_duplicates(
    subset=["product_id", "sale_date"]
).copy()
inventory = check_duplicates(inventory, "inventory", "inventory_id")
purchase_orders = check_duplicates(purchase_orders, "purchase_orders", "order_id")
shipments = check_duplicates(shipments, "shipments", "shipment_id")

# Validate sales
valid_product_ids = set(products["product_id"])

invalid_sales = sales[
    (sales["quantity_sold"] <= 0) |
    (~sales["product_id"].isin(valid_product_ids))
].copy()

invalid_sales["dataset"] = "sales"
invalid_sales["reason"] = "Invalid quantity or product ID"
rejected_records.append(invalid_sales)

sales = sales.drop(invalid_sales.index)
log_issue("sales", "Rejected records", len(invalid_sales))

# Validate inventory
invalid_inventory = inventory[
    (inventory["quantity_available"] < 0) |
    (~inventory["product_id"].isin(valid_product_ids))
].copy()

invalid_inventory["dataset"] = "inventory"
invalid_inventory["reason"] = "Invalid quantity or product ID"
rejected_records.append(invalid_inventory)

inventory = inventory.drop(invalid_inventory.index)
log_issue("inventory", "Rejected records", len(invalid_inventory))

# Validate purchase orders
valid_supplier_ids = set(suppliers["supplier_id"])

invalid_orders = purchase_orders[
    (purchase_orders["quantity"] <= 0) |
    (~purchase_orders["product_id"].isin(valid_product_ids)) |
    (~purchase_orders["supplier_id"].isin(valid_supplier_ids))
].copy()

invalid_orders["dataset"] = "purchase_orders"
invalid_orders["reason"] = "Invalid quantity, product ID or supplier ID"
rejected_records.append(invalid_orders)

purchase_orders = purchase_orders.drop(invalid_orders.index)
log_issue("purchase_orders", "Rejected records", len(invalid_orders))

# Validate shipments
valid_order_ids = set(purchase_orders["order_id"])

invalid_shipments = shipments[
    ~shipments["order_id"].isin(valid_order_ids)
].copy()

invalid_shipments["dataset"] = "shipments"
invalid_shipments["reason"] = "Unknown purchase order ID"
rejected_records.append(invalid_shipments)

shipments = shipments.drop(invalid_shipments.index)
log_issue("shipments", "Rejected records", len(invalid_shipments))

# Save cleaned datasets
cleaned_data = {
    "products.csv": products,
    "sales.csv": sales,
    "inventory.csv": inventory,
    "suppliers.csv": suppliers,
    "purchase_orders.csv": purchase_orders,
    "shipments.csv": shipments
}

for filename, dataframe in cleaned_data.items():
    dataframe.to_csv(CLEAN_DIR / filename, index=False)
    print(f"{filename}: {len(dataframe)} clean records")

# Save quality reports
pd.DataFrame(quality_logs).to_csv(
    REPORT_DIR / "data_quality_logs.csv", index=False
)

if rejected_records:
    rejected_data = pd.concat(rejected_records, ignore_index=True)
else:
    rejected_data = pd.DataFrame()

rejected_data.to_csv(
    REPORT_DIR / "rejected_records.csv", index=False
)

print("\nData cleaning completed successfully!")
print("Cleaned files saved in data/cleaned/")
print("Quality reports saved in reports/")
