from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    _tablename_ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    shipping_fee = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Shipping address
    shipping_street = Column(String(255))
    shipping_city = Column(String(100))
    shipping_county = Column(String(100))
    shipping_postal_code = Column(String(20))
    shipping_instructions = Column(Text)
    
    # Payment and order status
    payment_method = Column(String(20), nullable=False)  # mpesa, cash, card, bank
    payment_status = Column(String(20), default="pending")  # pending, paid, failed, refunded
    order_status = Column(String(20), default="pending")  # pending, confirmed, processing, shipped, delivered, cancelled
    
    notes = Column(Text)
    estimated_delivery = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    customer = relationship("User")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    _tablename_ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")