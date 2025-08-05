from sqlalchemy import Column, String, Text, DateTime, JSON, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import enum
from sqlalchemy import Enum

class OrderStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"
class UserRole(enum.Enum):
    admin = "admin"
    user = "user"
class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"    
    COD = "COD"  # Cash on Delivery
    Pre_paid = "Pre-paid"  # Pre-paid

# Define the base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    roles_permissions = Column(Enum(UserRole), nullable=False)

class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String(100), nullable=False)

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(String(20), nullable=False)
    category_id = Column(String(100), ForeignKey('categories.category_id'), nullable=False)
    product_metadata = Column(JSON, nullable=True)  # For additional product information
    count = Column(String(20), nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.product_id'), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    address_id = Column(String(36), ForeignKey('addresses.address_id'), nullable=False)
    quantity = Column(String(20), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
