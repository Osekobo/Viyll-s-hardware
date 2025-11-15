from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.middleware.auth import get_current_admin
from app.utils.email import send_contact_notification

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("/", response_model=ContactResponse)
def create_contact(contact_data: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**contact_data.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    # Send email notification
    send_contact_notification(contact_data.dict())
    
    return contact

@router.get("/", response_model=List[ContactResponse])
def get_contacts(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    query = db.query(Contact)
    
    if status:
        query = query.filter(Contact.status == status)
    
    offset = (page - 1) * limit
    contacts = query.order_by(Contact.created_at.desc()).offset(offset).limit(limit).all()
    
    return contacts

@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_status(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    for field, value in contact_data.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    
    db.commit()
    db.refresh(contact)
    return contact