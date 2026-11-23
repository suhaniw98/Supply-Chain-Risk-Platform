# Database Schema Documentation

## Overview

The database contains the following SQLAlchemy models:

## Table: `products`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| product_id | VARCHAR | Yes | No | No |
| product_name | VARCHAR | No | Yes | No |
| category | VARCHAR | No | Yes | No |
| unit_cost | FLOAT | No | Yes | No |

## Table: `suppliers`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| supplier_id | VARCHAR | Yes | No | No |
| supplier_name | VARCHAR | No | Yes | No |
| lead_time | INTEGER | No | Yes | No |
| status | VARCHAR | No | Yes | No |

## Table: `inventory`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| inventory_id | VARCHAR | Yes | No | No |
| product_id | VARCHAR | No | Yes | products.product_id |
| location_id | VARCHAR | No | Yes | No |
| quantity_available | INTEGER | No | Yes | No |

## Table: `purchase_orders`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| order_id | VARCHAR | Yes | No | No |
| supplier_id | VARCHAR | No | Yes | suppliers.supplier_id |
| product_id | VARCHAR | No | Yes | products.product_id |
| quantity | INTEGER | No | Yes | No |
| order_date | DATE | No | Yes | No |
| expected_date | DATE | No | Yes | No |
| status | VARCHAR | No | Yes | No |

## Table: `sales`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| id | INTEGER | Yes | No | No |
| product_id | VARCHAR | No | Yes | products.product_id |
| sale_date | DATE | No | Yes | No |
| quantity_sold | INTEGER | No | Yes | No |

## Table: `shipments`

| Column | Data Type | Primary Key | Nullable | Foreign Key |
|---|---|---|---|---|
| shipment_id | VARCHAR | Yes | No | No |
| order_id | VARCHAR | No | Yes | purchase_orders.order_id |
| dispatch_date | DATE | No | Yes | No |
| delivery_date | DATE | No | Yes | No |
| shipment_status | VARCHAR | No | Yes | No |

## Relationships

- `inventory.product_id` references `products.product_id`
- `purchase_orders.supplier_id` references `suppliers.supplier_id`
- `purchase_orders.product_id` references `products.product_id`
- `sales.product_id` references `products.product_id`
- `shipments.order_id` references `purchase_orders.order_id`