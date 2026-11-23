
import pytest
from fastapi.testclient import TestClient

import api.main as api_module

client = TestClient(api_module.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["database"] == "PostgreSQL"


def test_get_products(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_db",
        lambda query, params=None: [
            {"product_id": "P001", "product_name": "Notebook"}
        ]
    )

    response = client.get("/api/products")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P001"


def test_get_inventory(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_csv",
        lambda folder, filename: [
            {"product_id": "P001", "risk_level": "Critical"}
        ]
    )

    response = client.get("/api/inventory")

    assert response.status_code == 200
    assert response.json()[0]["risk_level"] == "Critical"


def test_get_forecast(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_csv",
        lambda folder, filename: [
            {"product_id": "P001", "predicted_quantity": 11.14},
            {"product_id": "P002", "predicted_quantity": 15.20}
        ]
    )

    response = client.get("/api/forecasts/P001")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["product_id"] == "P001"


def test_forecast_not_found(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_csv",
        lambda folder, filename: []
    )

    response = client.get("/api/forecasts/P999")

    assert response.status_code == 404


def test_supplier_performance(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_csv",
        lambda folder, filename: [
            {"supplier_id": "S001", "supplier_name": "ABC Suppliers"}
        ]
    )

    response = client.get("/api/suppliers/performance")

    assert response.status_code == 200
    assert response.json()[0]["supplier_id"] == "S001"


def test_purchase_orders(monkeypatch):
    monkeypatch.setattr(
        api_module,
        "load_csv",
        lambda folder, filename: [
            {"order_id": "PO002", "days_overdue": 3}
        ]
    )

    response = client.get("/api/purchase-orders")

    assert response.status_code == 200
    assert response.json()[0]["order_id"] == "PO002"


def test_risk_alerts(monkeypatch):
    def mock_load_csv(folder, filename):
        if filename == "inventory_risk_analysis.csv":
            return [
                {"product_id": "P001", "risk_level": "Critical"},
                {"product_id": "P002", "risk_level": "Normal"}
            ]

        if filename == "purchase_order_monitoring.csv":
            return [
                {"order_id": "PO002", "days_overdue": 3}
            ]

        return []

    monkeypatch.setattr(api_module, "load_csv", mock_load_csv)

    response = client.get("/api/alerts")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_analytics_summary(monkeypatch):
    def mock_load_db(query, params=None):
        if "products" in query:
            return [{"total": 10}]
        if "suppliers" in query:
            return [{"total": 5}]
        if "purchase_orders" in query:
            return [{"total": 5}]
        return []

    def mock_load_csv(folder, filename):
        if filename == "inventory_risk_analysis.csv":
            return [
                {"risk_level": "Critical"},
                {"risk_level": "High"},
                {"risk_level": "Normal"}
            ]

        if filename == "demand_forecast.csv":
            return [{"product_id": "P001"}] * 70

        if filename == "purchase_order_monitoring.csv":
            return [
                {"status": "In Transit", "days_overdue": 3},
                {"status": "Delayed", "days_overdue": 0}
            ]

        return []

    monkeypatch.setattr(api_module, "load_db", mock_load_db)
    monkeypatch.setattr(api_module, "load_csv", mock_load_csv)

    response = client.get("/api/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_products"] == 10
    assert data["total_suppliers"] == 5
    assert data["total_purchase_orders"] == 5
    assert data["inventory_records"] == 3
    assert data["forecast_records"] == 70
    assert data["critical_stock"] == 1
    assert data["high_risk_stock"] == 1
    assert data["overdue_orders"] == 2
