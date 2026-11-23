
import pandas as pd
import numpy as np
import runpy
from pathlib import Path


def test_demand_forecasting():
    project_dir = Path(__file__).resolve().parent.parent

    report_file = project_dir / "reports" / "demand_forecast.csv"

    # Run the forecasting script
    script_file = project_dir / "forecasting" / "demand_forecaster.py"

    runpy.run_path(str(script_file))

    # Check report file exists
    assert report_file.exists(), "Forecast report was not generated"

    forecast = pd.read_csv(report_file)

    # Check forecast is not empty
    assert not forecast.empty

    # Check required columns
    required_columns = [
        "product_id",
        "forecast_day",
        "forecast_date",
        "predicted_quantity",
        "selected_model",
        "moving_average_mae",
        "exponential_smoothing_mae",
        "moving_average_rmse",
        "exponential_smoothing_rmse"
    ]

    for column in required_columns:
        assert column in forecast.columns

    # Check number of products
    assert forecast["product_id"].nunique() == 10

    # Check 7 forecast records per product
    records_per_product = forecast.groupby("product_id").size()

    assert (records_per_product == 7).all()

    # Check total forecast records
    assert len(forecast) == 70

    # Check forecast days
    for product_id, group in forecast.groupby("product_id"):
        assert sorted(group["forecast_day"].tolist()) == list(range(1, 8))

    # Check predicted quantities are non-negative
    assert (forecast["predicted_quantity"] >= 0).all()

    # Check forecast dates are valid and in the future
    forecast_dates = pd.to_datetime(forecast["forecast_date"])

    assert forecast_dates.notna().all()
    assert (forecast_dates > pd.Timestamp.now().normalize()).all()

    # Check selected models
    valid_models = [
        "Moving Average",
        "Exponential Smoothing"
    ]

    assert forecast["selected_model"].isin(valid_models).all()

    # Check MAE and RMSE values
    metric_columns = [
        "moving_average_mae",
        "exponential_smoothing_mae",
        "moving_average_rmse",
        "exponential_smoothing_rmse"
    ]

    for column in metric_columns:
        assert np.isfinite(forecast[column]).all()
        assert (forecast[column] >= 0).all()

    print("\nForecasting tests completed successfully!")
