from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    email: str
    subject: str
    message: str

class ContactCreate(ContactBase):
    phone: Optional[str] = None

class ContactUpdate(BaseModel):
    status: Optional[str] = None
    response_message: Optional[str] = None

class ContactResponse(ContactBase):
    id: int
    phone: Optional[str]
    status: str
    response_message: Optional[str]
    replied_at: Optional[datetime]
    replied_by: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True