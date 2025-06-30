from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from enum import Enum
from datetime import datetime

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"
    COD = "COD"
    Pre_paid = "Pre-paid"

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    roles_permissions: UserRole

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    user_id: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True

class AddressBase(BaseModel):
    address: str
    city: str
    state: str
    country: str
    postal_code: str

class AddressCreate(AddressBase):
    user_id: str

class AddressRead(AddressBase):
    address_id: str
    user_id: str

class AddressUpdate(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    category: str

class CategoryRead(CategoryBase):
    pass

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: str
    category: str
    product_metadata: Optional[Any] = None
    count: str

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    product_id: str

class OrderBase(BaseModel):
    user_id: str
    product_id: str
    payment_status: PaymentStatus
    address_id: str
    quantity: str
    status: OrderStatus

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    order_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None