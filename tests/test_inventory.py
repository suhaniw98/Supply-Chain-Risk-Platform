
import pandas as pd
import runpy
from pathlib import Path


def test_inventory_optimization():

    project_dir = Path(__file__).resolve().parent.parent

    script_file = project_dir / "modules" / "inventory_optimizer.py"

    report_file = project_dir / "reports" / "inventory_risk_analysis.csv"

    # Run inventory optimization script
    runpy.run_path(str(script_file))

    # Check report exists
    assert report_file.exists(), "Inventory report not generated"

    # Load report
    inventory = pd.read_csv(report_file)

    # Check report is not empty
    assert not inventory.empty

    # Check total products
    assert len(inventory) == 10

    # Check required columns
    required_columns = [
        "product_id",
        "average_daily_demand",
        "open_order_quantity",
        "lead_time",
        "safety_stock",
        "reorder_point",
        "inventory_position",
        "risk_level",
        "suggested_replenishment"
    ]

    for column in required_columns:
        assert column in inventory.columns

    # Check risk levels
    valid_risks = ["Critical", "High", "Normal"]

    assert inventory["risk_level"].isin(valid_risks).all()

    # Check calculations
    assert (inventory["average_daily_demand"] >= 0).all()
    assert (inventory["open_order_quantity"] >= 0).all()
    assert (inventory["safety_stock"] >= 0).all()
    assert (inventory["reorder_point"] >= 0).all()
    assert (inventory["suggested_replenishment"] >= 0).all()

    # Check inventory position calculation
    expected_position = (
        inventory["quantity_available"]
        + inventory["open_order_quantity"]
    )

    assert (
        inventory["inventory_position"].round(2)
        == expected_position.round(2)
    ).all()

    # Check safety stock calculation
    expected_safety_stock = (
        inventory["average_daily_demand"] * 2
    )

    assert (
        inventory["safety_stock"].round(2)
        == expected_safety_stock.round(2)
    ).all()

    # Check suggested replenishment
    expected_replenishment = (
        inventory["average_daily_demand"] * 14
        - inventory["inventory_position"]
    ).clip(lower=0).round()

    assert (
        inventory["suggested_replenishment"]
        == expected_replenishment
    ).all()

    print("\nInventory optimization tests completed successfully!")
