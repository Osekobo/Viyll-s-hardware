from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    _tablename_ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    image = Column(String(255))
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Self-referential relationship for subcategories
    subcategories = relationship("Category")

class Product(Base):
    _tablename_ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    subcategory = Column(String(100))
    brand = Column(String(100))
    sku = Column(String(100), unique=True)
    images = Column(JSON)  # Store as JSON list of image URLs
    stock = Column(Integer, default=0)
    features = Column(JSON)  # Store as JSON list
    specifications = Column(JSON)  # Store as JSON object
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    tags = Column(JSON)  # Store as JSON list
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category")