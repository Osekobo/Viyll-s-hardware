from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    parent_id: Optional[int] = None
    display_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category_id: int
    stock: int = 0

class ProductCreate(ProductBase):
    compare_price: Optional[float] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    images: Optional[List[str]] = None
    features: Optional[List[str]] = None
    specifications: Optional[Dict] = None
    is_featured: bool = False
    tags: Optional[List[str]] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    compare_price: Optional[float] = None
    category_id: Optional[int] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    images: Optional[List[str]] = None
    stock: Optional[int] = None
    features: Optional[List[str]] = None
    specifications: Optional[Dict] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[str]] = None

class ProductResponse(ProductBase):
    id: int
    compare_price: Optional[float]
    subcategory: Optional[str]
    brand: Optional[str]
    sku: str
    images: Optional[List[str]]
    features: Optional[List[str]]
    specifications: Optional[Dict]
    is_active: bool
    is_featured: bool
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True