
import pandas as pd
import runpy
from pathlib import Path


def test_supplier_analysis():

    project_dir = Path(__file__).resolve().parent.parent

    script_file = project_dir / "modules" / "supplier_analysis.py"

    report_file = project_dir / "reports" / "supplier_performance.csv"

    # Run supplier analysis
    runpy.run_path(str(script_file))

    # Check report exists
    assert report_file.exists(), "Supplier report not generated"

    # Load report
    suppliers = pd.read_csv(report_file)

    # Check report is not empty
    assert not suppliers.empty

    # Check total suppliers
    assert len(suppliers) == 5

    # Check required columns
    required_columns = [
        "supplier_id",
        "supplier_name",
        "total_orders",
        "delivered_orders",
        "on_time_deliveries",
        "on_time_delivery_rate",
        "delayed_orders",
        "average_transit_days",
        "risk_level"
    ]

    for column in required_columns:
        assert column in suppliers.columns

    # Check unique supplier IDs
    assert suppliers["supplier_id"].is_unique

    # Check order counts
    assert (suppliers["total_orders"] >= 0).all()
    assert (suppliers["delivered_orders"] >= 0).all()
    assert (
        suppliers["delivered_orders"] <= suppliers["total_orders"]
    ).all()

    # Check delivery rate
    assert suppliers["on_time_delivery_rate"].between(0, 100).all()

    # Check risk levels
    valid_risks = ["High", "Medium", "Normal"]

    assert suppliers["risk_level"].isin(valid_risks).all()

    # Check delayed orders
    assert (suppliers["delayed_orders"] >= 0).all()

    # Check transit time
    transit_values = suppliers["average_transit_days"].dropna()

    assert (transit_values >= 0).all()

    print("\nSupplier analysis tests completed successfully!")
