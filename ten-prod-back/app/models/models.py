from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    USER = "user"
    FARMER = "farmer"
    COURIER = "courier"
    ADMIN = "admin"

class OrderStatus(str, enum.Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    hashed_password = Column(String)
    address = Column(String, nullable=True)
    role = Column(String, default=UserRole.USER.value)
    
    orders = relationship("Order", back_populates="user", foreign_keys="Order.user_id")
    assigned_orders = relationship("Order", back_populates="courier", foreign_keys="Order.courier_id")
    cart_items = relationship("CartItem", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    courier_location = relationship("CourierLocation", back_populates="courier", uselist=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Product", back_populates="supplier")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    discount_price = Column(Float, nullable=True)
    stock = Column(Integer, default=0)
    expiration_date = Column(DateTime, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_url = Column(String, nullable=True)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    farmer = relationship("User", foreign_keys=[farmer_id])
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    total_price = Column(Float)
    payment_method = Column(String)
    address = Column(String)
    status = Column(String, default=OrderStatus.CREATED.value)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="orders")
    courier = relationship("User", foreign_keys=[courier_id], back_populates="assigned_orders")
    items = relationship("OrderItem", back_populates="order")
    feedback = relationship("Feedback", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class CourierLocation(Base):
    __tablename__ = "courier_locations"
    courier_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    lat = Column(Float)
    lng = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    courier = relationship("User", back_populates="courier_location")

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    rating = Column(Integer)
    comment = Column(String, nullable=True)

    user = relationship("User", back_populates="feedbacks")
    order = relationship("Order", back_populates="feedback")

