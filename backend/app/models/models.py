from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String(100), nullable=False)
    store_identifier = Column(String(50), unique=True, nullable=False)
    admin_username = Column(String(50), nullable=False)
    admin_password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tables = relationship("Table", back_populates="store")
    categories = relationship("Category", back_populates="store")
    menus = relationship("Menu", back_populates="store")


class Table(Base):
    __tablename__ = "tables"

    table_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False)
    table_number = Column(Integer, nullable=False)
    table_password_hash = Column(String(255), nullable=False)
    current_session_id = Column(Integer, ForeignKey("table_sessions.session_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="tables")
    sessions = relationship("TableSession", back_populates="table", foreign_keys="TableSession.table_id")


class TableSession(Base):
    __tablename__ = "table_sessions"

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)
    session_start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    session_end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    table = relationship("Table", back_populates="sessions", foreign_keys=[table_id])
    orders = relationship("Order", back_populates="session")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False)
    category_name = Column(String(50), nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="categories")
    menus = relationship("Menu", back_populates="category")


class Menu(Base):
    __tablename__ = "menus"

    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    menu_name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    store = relationship("Store", back_populates="menus")
    category = relationship("Category", back_populates="menus")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.table_id"), nullable=False)
    session_id = Column(Integer, ForeignKey("table_sessions.session_id"), nullable=False)
    order_number = Column(String(20), nullable=False)
    total_amount = Column(Integer, nullable=False)
    order_status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    session = relationship("TableSession", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    menu_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    order = relationship("Order", back_populates="items")
