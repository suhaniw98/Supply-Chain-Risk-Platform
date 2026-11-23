
import pandas as pd
from pathlib import Path
from database.db_connection import engine

base_folder = Path("data")
cleaned_folder = base_folder / "cleaned"

# Import order follows the foreign-key dependencies
tables = {
    "products": ["products.csv", []],
    "suppliers": ["suppliers.csv", []],
    "inventory": ["inventory.csv", []],
    "purchase_orders": [
        "purchase_orders.csv",
        ["order_date", "expected_date"]
    ],
    "sales": ["sales.csv", ["sale_date"]],
    "shipments": [
        "shipments.csv",
        ["dispatch_date", "delivery_date"]
    ]
}

try:
    with engine.begin() as connection:

        for table_name, details in tables.items():
            filename, date_columns = details

            # Prefer cleaned CSV files when available
            cleaned_file = cleaned_folder / filename
            raw_file = base_folder / filename

            file_path = cleaned_file if cleaned_file.exists() else raw_file

            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Prevent duplicate imports
            existing_count = connection.exec_driver_sql(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).scalar()

            if existing_count > 0:
                raise ValueError(
                    f"{table_name} already contains data. "
                    "Import stopped to prevent duplicates."
                )

            df = pd.read_csv(file_path)

            for column in date_columns:
                df[column] = pd.to_datetime(
                    df[column], errors="coerce"
                ).dt.date

            df.to_sql(
                table_name,
                con=connection,
                if_exists="append",
                index=False
            )

            print(f"{table_name}: {len(df)} records imported")

    print("\nAll CSV data imported successfully!")

except Exception as error:
    print("\nData import failed:", error)
