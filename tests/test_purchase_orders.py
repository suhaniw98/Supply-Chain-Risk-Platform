
import pandas as pd
import runpy
from pathlib import Path


def test_purchase_order_monitoring():

    project_dir = Path(__file__).resolve().parent.parent

    script_file = (
        project_dir / "modules" / "purchase_order_monitor.py"
    )

    report_file = (
        project_dir / "reports" / "purchase_order_monitoring.csv"
    )

    # Run purchase order monitoring
    runpy.run_path(str(script_file))

    # Check report exists
    assert report_file.exists(), "Purchase order report not generated"

    # Load report
    orders = pd.read_csv(report_file)

    # Check report is not empty
    assert not orders.empty

    # Check total purchase orders
    assert len(orders) == 5

    # Check required columns
    required_columns = [
        "order_id",
        "product_id",
        "status",
        "expected_date",
        "is_overdue",
        "days_overdue",
        "quantity_available",
        "risk_level",
        "suggested_replenishment",
        "alert"
    ]

    for column in required_columns:
        assert column in orders.columns

    # Check unique order IDs
    assert orders["order_id"].is_unique

    # Check overdue values
    assert orders["is_overdue"].isin([True, False]).all()

    # Check overdue days are non-negative
    assert (orders["days_overdue"] >= 0).all()

    # Check non-overdue orders have zero overdue days
    assert (
        orders.loc[~orders["is_overdue"], "days_overdue"] == 0
    ).all()

    # Check alert types
    valid_alerts = [
        "Overdue Shipment",
        "Critical Inventory Risk",
        "Delayed Order",
        "Normal"
    ]

    assert orders["alert"].isin(valid_alerts).all()

    # Check overdue alert logic
    overdue_orders = orders[orders["is_overdue"]]

    assert (
        overdue_orders["alert"] == "Overdue Shipment"
    ).all()

    print("\nPurchase order monitoring tests completed successfully!")
