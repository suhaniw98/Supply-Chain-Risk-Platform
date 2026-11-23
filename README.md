# Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform

## 1. Project Overview

The **Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform** is a Python-based data analytics and monitoring solution designed to improve supply chain visibility and decision-making.

The system analyzes sales, inventory, suppliers, purchase orders, and shipment data to identify inventory risks, forecast future product demand, monitor supplier performance, and detect delayed purchase orders.

This project uses synthetic sample datasets generated for development, demonstration, and testing purposes.

## 2. Project Objectives

- Analyze historical sales and inventory data.
- Forecast product demand for the next 7 days.
- Identify critical and high-risk inventory levels.
- Calculate safety stock and reorder points.
- Monitor supplier delivery performance.
- Identify overdue purchase orders.
- Generate supply chain risk alerts.
- Display insights through an interactive dashboard.
- Provide supply chain information through REST API endpoints.
- Generate structured reports for business analysis.

## 3. Key Features

### 3.1 Data Integration and Cleaning

- CSV data loading and integration.
- Missing-value and duplicate handling.
- Data validation and quality checks.
- Data quality logs and rejected records.
- Integration of products, sales, inventory, suppliers, purchase orders, and shipments.
- Data dictionary documentation.

### 3.2 Demand Forecasting

- 7-day Moving Average.
- Simple Exponential Smoothing.
- Chronological train-test split.
- MAE and RMSE model evaluation.
- Automatic selection of the model with lower MAE.
- 7-day future demand predictions.
- Forecast evaluation reports.

### 3.3 Inventory Risk Analysis

- Average daily demand calculation.
- Safety stock calculation.
- Reorder point calculation.
- Inventory position monitoring.
- Critical, High, and Normal risk classification.
- Suggested replenishment quantity based on 14 days of demand.
- Consideration of existing purchase orders in inventory planning.

### 3.4 Supplier Performance Monitoring

- Total purchase orders.
- Delivered orders.
- On-time delivery rate.
- Average shipment transit time.
- Supplier performance analysis.
- Supplier risk classification.

### 3.5 Purchase Order Monitoring

- Purchase order status tracking.
- Overdue order identification.
- Days overdue calculation.
- Inventory-related alerts.
- Purchase order monitoring reports.

### 3.6 Interactive Dashboard

The dashboard provides the following sections:

- Dashboard Summary
- Inventory Risk Analysis
- Demand Forecasting
- Supplier Performance
- Purchase Order Monitoring
- Risk Alerts

Additional dashboard features include search, filtering, forecast date selection, and CSV export.

## 4. Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Forecasting | Statsmodels |
| Evaluation Metrics | Scikit-learn |
| Visualization | Plotly, Matplotlib |
| Backend API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| Testing | Pytest |
| API Testing | FastAPI TestClient, Postman |
| Development Tools | VS Code, pgAdmin 4 |

## 5. Project Architecture

The project follows a modular architecture in which data processing, forecasting, inventory analysis, database operations, API services, and dashboard visualization are handled separately.

```text
              INPUT CSV DATASETS
                     |
                     v
          DATA INTEGRATION & CLEANING
                     |
                     v
              DATA ANALYSIS
                     |
          +----------+----------+
          |          |          |
          v          v          v
      FORECAST   INVENTORY   SUPPLIER &
      ANALYSIS   OPTIMIZATION PO MONITORING
          |          |          |
          +----------+----------+
                     |
                     v
              POSTGRESQL DATABASE
                     |
                     v
                 FASTAPI
                     |
                     v
             INTERACTIVE DASHBOARD
                     |
                     v
              REPORTS & ALERTS
```

## 6. Project Structure

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
│   ├── inventory_optimizer.py
│   ├── supplier_analysis.py
│   ├── purchase_order_monitor.py
│   ├── forecast_evaluation.py
│   ├── generate_data_dictionary.py
│   └── generate_schema_documentation.py
│
├── forecasting/
│   └── demand_forecaster.py
│
├── reports/
│   ├── data_dictionary.csv
│   ├── database_schema.md
│   ├── demand_forecast.csv
│   ├── forecast_evaluation_report.csv
│   ├── forecast_evaluation_summary.csv
│   └── other generated reports
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
└── .gitignore
```

Note: The `.env` file is used for local database configuration and is excluded from GitHub.

## 7. Sample Dataset

The project uses synthetic sample datasets generated for development and testing.

| Dataset | Records |
|---|---:|
| Products | 10 |
| Suppliers | 5 |
| Sales | 900 |
| Inventory | 10 |
| Purchase Orders | 5 |
| Shipments | 5 |

The generated datasets are stored in the `data/` directory. Cleaned datasets are stored in `data/cleaned/`.

## 8. Database Configuration

The project uses PostgreSQL with SQLAlchemy ORM.

Create a PostgreSQL database named:

```sql
CREATE DATABASE supply_chain_db;
```

Configure the database credentials in your local `.env` file:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=supply_chain_db
```

Do not upload your actual `.env` file or database password to GitHub.

### Database Tables

The database contains six tables:

1. Products
2. Inventory
3. Suppliers
4. Purchase Orders
5. Sales
6. Shipments

Database schema documentation is available at:

`reports/database_schema.md`

## 9. Installation

Clone the repository or open the project folder.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the PostgreSQL database and local environment variables before running database-dependent components.

## 10. Running the Project

Run the following commands from the project root directory.

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
python modules/inventory_optimization.py
```

### Step 7: Run Supplier Analysis

```bash
python modules/supplier_analysis.py
```

### Step 8: Run Purchase Order Monitoring

```bash
python modules/purchase_order_monitor.py
```

### Step 9: Generate Forecast Evaluation Report

```bash
python modules/forecast_evaluation.py
```

### Step 10: Generate Data Dictionary

```bash
python modules/generate_data_dictionary.py
```

### Step 11: Generate Database Schema Documentation

```bash
python modules/generate_schema_documentation.py
```

### Step 12: Start FastAPI Server

```bash
uvicorn api.main:app --reload
```

API URL:

http://127.0.0.1:8000

Swagger API Documentation:

http://127.0.0.1:8000/docs

### Step 13: Open Dashboard

Open `dashboard/index.html` using VS Code Live Server.

Example:

http://127.0.0.1:5500

## 11. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/api/products` | Retrieve product records |
| GET | `/api/inventory` | Retrieve inventory risk details |
| GET | `/api/forecasts/{product_id}` | Retrieve product demand forecast |
| GET | `/api/suppliers/performance` | Retrieve supplier performance |
| GET | `/api/purchase-orders` | Retrieve purchase order monitoring |
| GET | `/api/alerts` | Retrieve supply chain risk alerts |
| GET | `/api/analytics/summary` | Retrieve dashboard summary |

## 12. Forecast Evaluation

The project compares two forecasting methods:

- Moving Average
- Simple Exponential Smoothing

Model evaluation uses Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

The generated evaluation reports contain the model comparison results.

### Evaluation Summary

| Metric | Moving Average | Exponential Smoothing |
|---|---:|---:|
| Average MAE | 2.335 | 2.069 |
| Average RMSE | 2.801 | 2.706 |

Based on the calculated evaluation metrics, Exponential Smoothing achieved lower average MAE and RMSE in this evaluation.

Note: These metrics represent the project's model evaluation results. They should not be interpreted as verified accuracy against future actual demand.

## 13. Testing

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
| **Total** | **13** |

**Final Result: 13 Tests Passed**

## 14. Reports Generated

The system generates the following reports:

### Data Quality and Analysis

- `data_quality_logs.csv`
- `rejected_records.csv`
- `sales_analysis.csv`
- `product_sales_summary.csv`
- `daily_demand_summary.csv`
- `monthly_sales_trend.csv`
- `purchase_analysis.csv`
- `shipment_analysis.csv`

### Forecasting

- `demand_forecast.csv`
- `forecast_evaluation_report.csv`
- `forecast_evaluation_summary.csv`

### Inventory and Supplier Analysis

- `inventory_analysis.csv`
- `inventory_risk_analysis.csv`
- `supplier_performance.csv`
- `purchase_order_monitoring.csv`

### Documentation

- `data_dictionary.csv`
- `database_schema.md`

All generated reports are stored in the `reports/` directory.

## 15. Assumptions and Limitations

- The project uses synthetic sample data and does not represent live business operations.
- Forecasts are generated using historical sample sales data.
- Forecast evaluation metrics are based on the implemented chronological validation process.
- Actual future forecast accuracy cannot be confirmed until future demand data becomes available.
- Supplier performance results are based on the available sample purchase orders and shipments.
- Risk classifications and replenishment recommendations depend on the implemented business rules and assumptions.
- The application is intended for demonstration and development purposes.

## 16. Future Enhancements

- Integration with live supply chain data sources.
- More advanced demand forecasting models.
- Forecast versus actual demand monitoring.
- Additional supplier performance history.
- Automated notifications for critical inventory and delayed orders.
- Cloud deployment and production database hosting.

## 17. Conclusion

The Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform combines data integration, demand forecasting, inventory optimization, supplier performance monitoring, and purchase order tracking into one solution.

It provides data-driven insights through an interactive dashboard, REST API services, database integration, and generated analytical reports.

The project demonstrates how Python-based analytics and automation can support supply chain visibility, inventory planning, and operational risk monitoring.

---

**Project:** Enterprise Supply Chain Risk Intelligence & Demand Forecasting Platform

**Project ID:** PY-W3-008

**Version:** 1.0

**Status:** Development and Testing Completed
