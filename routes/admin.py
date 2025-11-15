from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.contact import Contact
from app.middleware.auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    # Get total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # Get total products
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar()
    
    # Get total orders
    total_orders = db.query(func.count(Order.id)).scalar()
    
    # Get total revenue
    total_revenue_result = db.query(func.sum(Order.total_amount)).filter(Order.payment_status == 'paid').first()
    total_revenue = total_revenue_result[0] or 0
    
    # Get pending orders
    pending_orders = db.query(func.count(Order.id)).filter(Order.order_status == 'pending').scalar()
    
    # Get new contacts
    new_contacts = db.query(func.count(Contact.id)).filter(Contact.status == 'new').scalar()
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "new_contacts": new_contacts
    }