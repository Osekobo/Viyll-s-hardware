from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    price: float
    total: float
    product_name: str

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    shipping_street: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_county: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    shipping_instructions: Optional[str] = None
    payment_method: str
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    order_status: Optional[str] = None
    payment_status: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    order_number: str
    customer_id: int
    subtotal: float
    tax: float
    shipping_fee: float
    total_amount: float
    payment_status: str
    order_status: str
    estimated_delivery: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponse]
    customer_name: str

    class Config:
        from_attributes = True