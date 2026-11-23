
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Products
products = pd.DataFrame([
    [f"P{i:03}", name, category, cost]
    for i, (name, category, cost) in enumerate([
        ("Laptop", "Electronics", 45000),
        ("Mouse", "Electronics", 500),
        ("Keyboard", "Electronics", 1200),
        ("Office Chair", "Furniture", 5500),
        ("Desk", "Furniture", 7000),
        ("Notebook", "Stationery", 50),
        ("Pen", "Stationery", 10),
        ("Printer", "Electronics", 12000),
        ("Monitor", "Electronics", 15000),
        ("Bookshelf", "Furniture", 4000),
    ], start=1)],
    columns=["product_id", "product_name", "category", "unit_cost"]
)

# Suppliers
suppliers = pd.DataFrame([
    ["S001", "ABC Suppliers", 5, "Active"],
    ["S002", "Global Traders", 7, "Active"],
    ["S003", "Reliable Distributors", 4, "Active"],
    ["S004", "Metro Wholesale", 10, "Active"],
    ["S005", "Prime Logistics", 6, "Active"],
], columns=["supplier_id", "supplier_name", "lead_time", "status"])

# Daily sales
dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=90)
sales_rows = []

for product_id in products["product_id"]:
    for date in dates:
        sales_rows.append([
            product_id,
            date,
            int(pd.Series([5, 8, 10, 12, 15]).sample(
                random_state=int(date.strftime("%j")) +
                int(product_id[-3:])
            ).iloc[0])
        ])

sales = pd.DataFrame(
    sales_rows,
    columns=["product_id", "sale_date", "quantity_sold"]
)

# Inventory
inventory = pd.DataFrame([
    [f"I{i:03}", product_id, "LOC001", quantity]
    for i, (product_id, quantity) in enumerate(
        zip(products["product_id"], [20, 150, 45, 12, 8, 300, 500, 15, 18, 10]),
        start=1
    )
], columns=["inventory_id", "product_id", "location_id", "quantity_available"])

# Purchase Orders
purchase_orders = pd.DataFrame([
    ["PO001", "S001", "P001", 50, "2026-11-01", "2026-11-06", "Delivered"],
    ["PO002", "S002", "P002", 100, "2026-11-05", "2026-11-12", "In Transit"],
    ["PO003", "S003", "P003", 40, "2026-11-02", "2026-11-06", "Delayed"],
    ["PO004", "S004", "P004", 25, "2026-11-10", "2026-11-20", "Pending"],
    ["PO005", "S005", "P005", 30, "2026-11-08", "2026-11-14", "In Transit"],
], columns=[
    "order_id", "supplier_id", "product_id", "quantity",
    "order_date", "expected_date", "status"
])

# Shipments
shipments = pd.DataFrame([
    ["SH001", "PO001", "2026-11-02", "2026-11-05", "Delivered"],
    ["SH002", "PO002", "2026-11-06", None, "In Transit"],
    ["SH003", "PO003", "2026-11-03", None, "Delayed"],
    ["SH004", "PO004", None, None, "Pending"],
    ["SH005", "PO005", "2026-11-09", None, "In Transit"],
], columns=[
    "shipment_id", "order_id", "dispatch_date",
    "delivery_date", "shipment_status"
])

# Save all datasets
datasets = {
    "products.csv": products,
    "sales.csv": sales,
    "inventory.csv": inventory,
    "suppliers.csv": suppliers,
    "purchase_orders.csv": purchase_orders,
    "shipments.csv": shipments,
}

for filename, dataframe in datasets.items():
    dataframe.to_csv(DATA_DIR / filename, index=False)
    print(f"{filename} created: {len(dataframe)} records")

print("\nAll sample datasets generated successfully!")