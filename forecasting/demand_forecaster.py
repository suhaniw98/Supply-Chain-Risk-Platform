
import pandas as pd
from pathlib import Path
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load sales data
sales = pd.read_csv(DATA_DIR / "sales.csv")

sales["sale_date"] = pd.to_datetime(
    sales["sale_date"],
    errors="coerce"
)

sales["quantity_sold"] = pd.to_numeric(
    sales["quantity_sold"],
    errors="coerce"
)

sales = sales.dropna(
    subset=["product_id", "sale_date", "quantity_sold"]
)

forecast_results = []

# Get today's date
today = pd.Timestamp.now().normalize()

# Process each product separately
for product_id in sales["product_id"].unique():

    product_data = sales[
        sales["product_id"] == product_id
    ].sort_values("sale_date")

    # Combine sales occurring on the same date
    daily_sales = (
        product_data.groupby("sale_date")["quantity_sold"]
        .sum()
        .asfreq("D", fill_value=0)
    )

    if len(daily_sales) < 15:
        print(f"Skipping {product_id}: Insufficient sales history")
        continue

    # Chronological train-test split
    train = daily_sales.iloc[:-14]
    test = daily_sales.iloc[-14:]

    if len(train) < 7:
        continue

    # Moving Average Forecast
    moving_average_value = train.tail(7).mean()

    moving_average_forecast = np.repeat(
        moving_average_value,
        len(test)
    )

    # Exponential Smoothing Forecast
    model = SimpleExpSmoothing(
        train,
        initialization_method="estimated"
    ).fit()

    exponential_forecast = model.forecast(len(test))

    # Model Evaluation
    ma_mae = mean_absolute_error(
        test,
        moving_average_forecast
    )

    es_mae = mean_absolute_error(
        test,
        exponential_forecast
    )

    ma_rmse = np.sqrt(
        mean_squared_error(
            test,
            moving_average_forecast
        )
    )

    es_rmse = np.sqrt(
        mean_squared_error(
            test,
            exponential_forecast
        )
    )

    # Select best model using MAE
    if es_mae < ma_mae:

        best_model = "Exponential Smoothing"

        selected_forecast = model.forecast(7)

    else:

        best_model = "Moving Average"

        selected_forecast = np.repeat(
            moving_average_value,
            7
        )

    # Generate future dates from tomorrow
    last_sale_date = daily_sales.index.max()

    forecast_start_date = max(
        last_sale_date.normalize(),
        today
    ) + pd.Timedelta(days=1)

    future_dates = pd.date_range(
        start=forecast_start_date,
        periods=7,
        freq="D"
    )

    # Save forecast results
    for day, (forecast_date, predicted_value) in enumerate(
        zip(future_dates, selected_forecast),
        start=1
    ):

        forecast_results.append({

            "product_id": product_id,

            "forecast_day": day,

            "forecast_date": forecast_date.strftime("%Y-%m-%d"),

            "predicted_quantity": max(
                0,
                round(float(predicted_value), 2)
            ),

            "selected_model": best_model,

            "moving_average_mae": round(float(ma_mae), 2),

            "exponential_smoothing_mae": round(float(es_mae), 2),

            "moving_average_rmse": round(float(ma_rmse), 2),

            "exponential_smoothing_rmse": round(float(es_rmse), 2)
        })


# Create final forecast DataFrame
forecast_df = pd.DataFrame(forecast_results)

if forecast_df.empty:
    raise ValueError("No forecast results generated. Check sales data.")

# Save forecast report
forecast_df.to_csv(
    REPORT_DIR / "demand_forecast.csv",
    index=False
)

# Display summary
print("\nDemand Forecasting Summary")
print("--------------------------")

print("Products forecasted:", forecast_df["product_id"].nunique())

print("Forecast horizon: 7 days")

print("Forecast start date:", forecast_df["forecast_date"].min())

print("Forecast end date:", forecast_df["forecast_date"].max())

print("Total forecast records:", len(forecast_df))

print("\nSelected Model Summary:")
print(
    forecast_df.groupby("selected_model")["product_id"]
    .nunique()
)

print("\nSample Forecast Results:")
print(
    forecast_df[
        [
            "product_id",
            "forecast_date",
            "predicted_quantity",
            "selected_model"
        ]
    ].head(10).to_string(index=False)
)

print("\nForecasting completed successfully!")
