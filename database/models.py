
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey
from database.db_connection import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True)
    product_name = Column(String)
    category = Column(String)
    unit_cost = Column(Float)


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"))
    location_id = Column(String)
    quantity_available = Column(Integer)


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(String, primary_key=True)
    supplier_name = Column(String)
    lead_time = Column(Integer)
    status = Column(String)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    order_id = Column(String, primary_key=True)
    supplier_id = Column(String, ForeignKey("suppliers.supplier_id"))
    product_id = Column(String, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    order_date = Column(Date)
    expected_date = Column(Date)
    status = Column(String)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, ForeignKey("products.product_id"))
    sale_date = Column(Date)
    quantity_sold = Column(Integer)


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("purchase_orders.order_id"))
    dispatch_date = Column(Date)
    delivery_date = Column(Date)
    shipment_status = Column(String)
