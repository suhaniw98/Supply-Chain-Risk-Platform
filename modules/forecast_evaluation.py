
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "reports" / "demand_forecast.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "forecast_evaluation_report.csv"
SUMMARY_FILE = BASE_DIR / "reports" / "forecast_evaluation_summary.csv"

df = pd.read_csv(INPUT_FILE)

# Metrics are repeated for each forecast day.
# Keep one record per product for evaluation.
evaluation = df.drop_duplicates(subset=["product_id"]).copy()

metric_columns = [
    "moving_average_mae",
    "exponential_smoothing_mae",
    "moving_average_rmse",
    "exponential_smoothing_rmse"
]

evaluation[metric_columns] = evaluation[metric_columns].apply(
    pd.to_numeric, errors="coerce"
)

evaluation["best_model_by_mae"] = evaluation.apply(
    lambda row: (
        "Moving Average"
        if row["moving_average_mae"] <= row["exponential_smoothing_mae"]
        else "Exponential Smoothing"
    ),
    axis=1
)

evaluation = evaluation[
    [
        "product_id",
        "selected_model",
        "best_model_by_mae",
        "moving_average_mae",
        "exponential_smoothing_mae",
        "moving_average_rmse",
        "exponential_smoothing_rmse"
    ]
]

evaluation.to_csv(OUTPUT_FILE, index=False)

summary = pd.DataFrame([
    {
        "metric": "Average MAE",
        "moving_average": evaluation["moving_average_mae"].mean(),
        "exponential_smoothing": evaluation["exponential_smoothing_mae"].mean()
    },
    {
        "metric": "Average RMSE",
        "moving_average": evaluation["moving_average_rmse"].mean(),
        "exponential_smoothing": evaluation["exponential_smoothing_rmse"].mean()
    }
])

summary.to_csv(SUMMARY_FILE, index=False)

print("Forecast Evaluation Report Generated Successfully!")
print("Products Evaluated:", len(evaluation))
print("\nModel Evaluation Summary:")
print(summary.to_string(index=False))
print("\nSaved:", OUTPUT_FILE)
print("Saved:", SUMMARY_FILE)
