
# Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform

## 1. Project Overview

The Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform is a Python-based data analytics and monitoring solution designed to improve supply chain visibility and decision-making.

The system analyzes sales, inventory, suppliers, purchase orders, and shipment data to identify inventory risks, forecast future product demand, monitor supplier performance, and detect delayed purchase orders.

This project uses synthetic sample datasets for demonstration and testing purposes.

## 2. Project Objectives

- Analyze historical sales and inventory data.
- Forecast product demand for the next 7 days.
- Identify critical and high-risk inventory levels.
- Calculate safety stock and reorder points.
- Monitor supplier delivery performance.
- Identify overdue purchase orders.
- Generate supply chain risk alerts.
- Display insights through an interactive dashboard.
- Provide data through REST API endpoints.

## 3. Key Features

### Data Integration
- CSV data loading and cleaning.
- Missing value and duplicate handling.
- Data quality logs and rejected records.
- Integration of sales, products, inventory, suppliers, and shipments.

### Demand Forecasting
- 7-day Moving Average.
- Simple Exponential Smoothing.
- Chronological train-test split.
- MAE and RMSE model evaluation.
- Automatic selection of the model with lower MAE.
- 7-day future demand predictions.

### Inventory Risk Analysis
- Average daily demand calculation.
- Safety stock calculation.
- Reorder point calculation.
- Inventory position monitoring.
- Critical, High, and Normal risk classification.
- Suggested replenishment quantity for 14 days of demand.

### Supplier Performance Monitoring
- Total purchase orders.
- Delivered orders.
- On-time delivery rate.
- Average shipment transit time.
- Supplier risk classification.

### Purchase Order Monitoring
- Purchase order status tracking.
- Overdue order identification.
- Days overdue calculation.
- Inventory-related alerts.
- Purchase order monitoring reports.

### Interactive Dashboard
- Dashboard summary.
- Inventory risk analysis.
- Demand forecasting.
- Supplier performance.
- Purchase order monitoring.
- Risk alerts.

## 4. Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Forecasting | Statsmodels |
| Machine Learning Metrics | Scikit-learn |
| Visualization | Plotly, Matplotlib |
| Backend API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest |
| API Testing | FastAPI TestClient, Postman |
| Development Tools | VS Code, pgAdmin 4 |

## 5. Project Structure

```text
Week_3_Supply_Chain_Platform/
│
├── api/
│   └── main.py
│
├── dashboard/
│   └── index.html
│
├── data/
│   ├── cleaned/
│   └── *.csv
│
├── database/
│   ├── __init__.py
│   ├── db_connection.py
│   └── models.py
│
├── modules/
│   ├── generate_sample_data.py
│   ├── data_integration.py
│   ├── data_joining.py
│   ├── demand_analysis.py
│   ├── inventory_optimization.py
│   ├── supplier_analysis.py
│   └── purchase_order_monitoring.py
│
├── forecasting/
│   └── demand_forecaster.py
│
├── reports/
│
├── tests/
│   ├── test_api.py
│   ├── test_forecasting.py
│   ├── test_inventory.py
│   ├── test_supplier.py
│   └── test_purchase_orders.py
│
├── requirements.txt
├── README.md
└── .env
```

## 6. Sample Dataset

The project uses synthetic sample data generated for development and testing.

| Dataset | Records |
|---|---:|
| Products | 10 |
| Suppliers | 5 |
| Sales | 900 |
| Inventory | 10 |
| Purchase Orders | 5 |
| Shipments | 5 |

## 7. Database Configuration

The project uses PostgreSQL with SQLAlchemy.

Create a PostgreSQL database named:

```text
supply_chain_db
```

Configure the database credentials in the `.env` file:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=supply_chain_db
```

Do not upload your actual `.env` file or database password to GitHub.

## 8. Installation

Clone the repository or open the project folder.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 9. Running the Project

### Step 1: Generate Sample Data

```bash
python modules/generate_sample_data.py
```

### Step 2: Run Data Integration

```bash
python modules/data_integration.py
```

### Step 3: Run Data Joining

```bash
python modules/data_joining.py
```

### Step 4: Run Demand Analysis

```bash
python modules/demand_analysis.py
```

### Step 5: Run Demand Forecasting

```bash
python forecasting/demand_forecaster.py
```

### Step 6: Run Inventory Optimization

```bash
python modules/inventory_optimizer.py
```

### Step 7: Run Supplier Analysis

```bash
python modules/supplier_analysis.py
```

### Step 8: Run Purchase Order Monitoring

```bash
python modules/purchase_order_monitor.py
```

### Step 9: Start FastAPI Server

```bash
uvicorn api.main:app --reload
```

API URL:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs

### Step 10: Open Dashboard

Open `dashboard/index.html` using VS Code Live Server.

Example:

http://127.0.0.1:5500

## 10. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | API status |
| GET | /api/products | Get product records |
| GET | /api/inventory | Get inventory risk details |
| GET | /api/forecasts/{product_id} | Get product demand forecast |
| GET | /api/suppliers/performance | Get supplier performance |
| GET | /api/purchase-orders | Get purchase order monitoring |
| GET | /api/alerts | Get supply chain risk alerts |
| GET | /api/analytics/summary | Get dashboard summary |

## 11. Testing

The project uses Pytest for automated testing.

Run all test cases:

```bash
python -m pytest tests/ -v
```

### Final Testing Results

| Test Module | Passed |
|---|---:|
| API Testing | 9 |
| Demand Forecasting | 1 |
| Inventory Optimization | 1 |
| Supplier Analysis | 1 |
| Purchase Order Monitoring | 1 |
| Total | 13 |

**Final Result: 13 Tests Passed**

## 12. Reports Generated

The system generates the following reports:

- data_quality_logs.csv
- rejected_records.csv
- sales_analysis.csv
- inventory_analysis.csv
- purchase_analysis.csv
- shipment_analysis.csv
- product_sales_summary.csv
- daily_demand_summary.csv
- monthly_sales_trend.csv
- demand_forecast.csv
- inventory_risk_analysis.csv
- supplier_performance.csv
- purchase_order_monitoring.csv

## 13. Conclusion

The Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform combines data integration, demand forecasting, inventory optimization, supplier performance monitoring, and purchase order tracking into one solution.

It helps identify potential supply chain risks and supports better inventory and operational decisions through data-driven insights.

---

**Project:** Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform

**Version:** 1.0

**Status:** Development and Testing Completed
