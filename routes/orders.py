from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.middleware.auth import get_current_user, get_current_admin
import random
import string

router = APIRouter(prefix="/orders", tags=["orders"])

def generate_order_number():
    return 'KIONE-ORD-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Validate products and calculate totals
    subtotal = 0
    order_items = []
    
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Insufficient stock for {product.name}. Available: {product.stock}"
            )
        
        item_total = product.price * item.quantity
        subtotal += item_total
        
        # Update product stock
        product.stock -= item.quantity
        
        order_items.append(OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
            total=item_total
        ))
    
    # Calculate tax and shipping
    tax = subtotal * 0.16  # 16% VAT
    shipping_fee = 0 if subtotal > 5000 else 300  # Free shipping above 5000 KES
    total_amount = subtotal + tax + shipping_fee
    
    # Create order
    order = Order(
        order_number=generate_order_number(),
        customer_id=user.id,
        subtotal=subtotal,
        tax=tax,
        shipping_fee=shipping_fee,
        total_amount=total_amount,
        shipping_street=order_data.shipping_street,
        shipping_city=order_data.shipping_city,
        shipping_county=order_data.shipping_county,
        shipping_postal_code=order_data.shipping_postal_code,
        shipping_instructions=order_data.shipping_instructions,
        payment_method=order_data.payment_method,
        notes=order_data.notes
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Add order items
    for item in order_items:
        item.order_id = order.id
        db.add(item)
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/my-orders", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.customer_id == user.id).order_by(Order.created_at.desc()).all()
    return orders

@router.get("/", response_model=List[OrderResponse])
def get_all_orders(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders

@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for field, value in order_data.dict(exclude_unset=True).items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order