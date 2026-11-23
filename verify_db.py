
from sqlalchemy import text
from database.db_connection import engine

tables = [
    "products",
    "suppliers",
    "inventory",
    "purchase_orders",
    "sales",
    "shipments"
]

try:
    with engine.connect() as connection:
        print("DATABASE VERIFICATION")
        print("-" * 35)

        total_records = 0

        for table in tables:
            result = connection.execute(
                text(f'SELECT COUNT(*) FROM "{table}"')
            )
            count = result.scalar()

            total_records += count

            print(f"{table}: {count} records")

        print("-" * 35)
        print(f"Total Records: {total_records}")
        print("Database verification completed!")

except Exception as error:
    print("Verification failed:", error)