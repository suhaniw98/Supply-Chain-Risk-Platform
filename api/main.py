
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database.db_connection import engine


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "reports"


# FastAPI application
app = FastAPI(
    title="Supply Chain Risk Intelligence API",
    description="Inventory, demand forecasting and supplier monitoring",
    version="1.1.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load data from PostgreSQL
def load_db(query, params=None):
    try:
        with engine.connect() as connection:
            data = pd.read_sql_query(
                text(query),
                connection,
                params=params or {}
            )

        data = data.astype(object).where(pd.notna(data), None)
        return data.to_dict(orient="records")

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(error)}"
        )


# Load data from CSV reports
def load_csv(folder, filename):
    file_path = folder / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{filename} not found. Generate the report first."
        )

    data = pd.read_csv(file_path)
    data = data.astype(object).where(pd.notna(data), None)

    return data.to_dict(orient="records")


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Supply Chain Risk Intelligence API is running",
        "database": "PostgreSQL",
        "docs": "/docs"
    }


# Get all products from PostgreSQL
@app.get("/api/products")
def get_products():
    return load_db(
        "SELECT * FROM products ORDER BY product_id"
    )


# Get inventory risk details from report
@app.get("/api/inventory")
def get_inventory():
    return load_csv(REPORT_DIR, "inventory_risk_analysis.csv")


# Get demand forecast for a product
@app.get("/api/forecasts/{product_id}")
def get_forecast(product_id: str):
    forecasts = load_csv(REPORT_DIR, "demand_forecast.csv")

    result = [
        item for item in forecasts
        if str(item.get("product_id")) == product_id
    ]

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Forecast not found for this product"
        )

    return result


# Get supplier performance
@app.get("/api/suppliers/performance")
def get_supplier_performance():
    return load_csv(REPORT_DIR, "supplier_performance.csv")


# Get purchase order monitoring
@app.get("/api/purchase-orders")
def get_purchase_orders():
    return load_csv(REPORT_DIR, "purchase_order_monitoring.csv")


# Get risk alerts
@app.get("/api/alerts")
def get_alerts():
    inventory = load_csv(
        REPORT_DIR,
        "inventory_risk_analysis.csv"
    )

    purchase_orders = load_csv(
        REPORT_DIR,
        "purchase_order_monitoring.csv"
    )

    alerts = []

    for item in inventory:
        risk = str(item.get("risk_level", "")).lower()

        if risk in ["critical", "high"]:
            alerts.append({
                "type": "Inventory Risk",
                "product_id": item.get("product_id"),
                "risk_level": item.get("risk_level"),
                "message": f"Stock risk detected for {item.get('product_id')}"
            })

    for order in purchase_orders:
        try:
            overdue_days = float(order.get("days_overdue") or 0)
        except (ValueError, TypeError):
            overdue_days = 0

        if overdue_days > 0:
            alerts.append({
                "type": "Purchase Order Delay",
                "order_id": order.get("order_id"),
                "days_overdue": overdue_days,
                "message": f"Purchase order {order.get('order_id')} is overdue"
            })

    return alerts


# Dashboard summary
@app.get("/api/analytics/summary")
def get_analytics_summary():

    # Raw data counts from PostgreSQL
    products = load_db(
        "SELECT COUNT(*) AS total FROM products"
    )

    suppliers = load_db(
        "SELECT COUNT(*) AS total FROM suppliers"
    )

    orders = load_db(
        "SELECT COUNT(*) AS total FROM purchase_orders"
    )

    # Report data from CSV
    inventory = load_csv(
        REPORT_DIR,
        "inventory_risk_analysis.csv"
    )

    forecasts = load_csv(
        REPORT_DIR,
        "demand_forecast.csv"
    )

    critical_count = sum(
        1 for item in inventory
        if str(item.get("risk_level", "")).lower() == "critical"
    )

    high_count = sum(
        1 for item in inventory
        if str(item.get("risk_level", "")).lower() == "high"
    )

    purchase_orders = load_csv(
        REPORT_DIR,
        "purchase_order_monitoring.csv"
    )

    overdue_count = 0

    for order in purchase_orders:
        try:
            overdue_days = float(order.get("days_overdue") or 0)
        except (ValueError, TypeError):
            overdue_days = 0

        if (
            str(order.get("status", "")).lower() == "delayed"
            or overdue_days > 0
        ):
            overdue_count += 1

    return {
        "total_products": products[0]["total"],
        "inventory_records": len(inventory),
        "forecast_records": len(forecasts),
        "total_suppliers": suppliers[0]["total"],
        "total_purchase_orders": orders[0]["total"],
        "critical_stock": critical_count,
        "high_risk_stock": high_count,
        "overdue_orders": overdue_count
    }
