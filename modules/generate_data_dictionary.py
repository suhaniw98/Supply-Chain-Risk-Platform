
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

dictionary = {
    "products.csv": {
        "product_id": "Unique identifier of the product",
        "product_name": "Name of the product",
        "category": "Category to which the product belongs",
        "unit_cost": "Cost of one unit of the product"
    },
    "inventory.csv": {
        "inventory_id": "Unique identifier of the inventory record",
        "product_id": "Identifier of the product",
        "location_id": "Identifier of the inventory location",
        "quantity_available": "Quantity of product currently available"
    },
    "sales.csv": {
        "product_id": "Identifier of the sold product",
        "sale_date": "Date on which the sale occurred",
        "quantity_sold": "Quantity of product sold"
    },
    "purchase_orders.csv": {
        "order_id": "Unique identifier of the purchase order",
        "supplier_id": "Identifier of the supplier",
        "product_id": "Identifier of the ordered product",
        "quantity": "Quantity requested in the purchase order",
        "order_date": "Date on which the order was placed",
        "expected_date": "Expected delivery date of the order",
        "status": "Current status of the purchase order"
    },
    "shipments.csv": {
        "shipment_id": "Unique identifier of the shipment",
        "order_id": "Identifier of the related purchase order",
        "dispatch_date": "Date on which the shipment was dispatched",
        "delivery_date": "Date on which the shipment was delivered",
        "shipment_status": "Current status of the shipment"
    },
    "suppliers.csv": {
        "supplier_id": "Unique identifier of the supplier",
        "supplier_name": "Name of the supplier",
        "lead_time": "Supplier lead time in days",
        "status": "Current status of the supplier"
    }
}

records = []

for filename, columns in dictionary.items():
    file_path = DATA_DIR / filename
    df = pd.read_csv(file_path)

    for column, description in columns.items():
        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' missing in {filename}"
            )

        records.append({
            "dataset": filename,
            "column_name": column,
            "data_type": str(df[column].dtype),
            "description": description
        })

result = pd.DataFrame(records)

output_file = REPORT_DIR / "data_dictionary.csv"
result.to_csv(output_file, index=False)

print("Data Dictionary Generated Successfully!")
print("Total Datasets:", len(dictionary))
print("Total Columns:", len(result))
print("Saved:", output_file)
