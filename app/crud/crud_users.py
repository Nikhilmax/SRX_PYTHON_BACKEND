from sqlalchemy.orm import Session
from app.db.models import User, Address
from app.schemas import UserCreate, UserUpdate, AddressCreate, AddressUpdate
from app.core.security import hash_password, verify_password
import re
from fastapi import HTTPException


def create_user(db: Session, user: UserCreate):
    # Validate email format
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, user.email):
        raise HTTPException(status_code=422, detail="Invalid email format.")
    # password validation and hashing
    password_regex = r'^(?=.*[A-Za-z])(?=.*\d).{8,}$'
    if not re.match(password_regex, user.password):
        raise HTTPException(
            status_code=422,
            detail="Password must be at least 8 characters long and contain both letters and numbers."
        )
    hashed_password = hash_password(user.password)
    #check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_password,
        roles_permissions=user.roles_permissions,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user_email: str, user_update: UserUpdate):
    db_user = get_user_by_email(db, email=user_email)
    if not db_user:
        return None

    if user_update.full_name:
        db_user.full_name = user_update.full_name
    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_email: str, user_password: str):
    db_user = get_user_by_email(db, email=user_email)
    if not db_user:
        return None

    if not verify_password(user_password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password.")

    db.delete(db_user)
    db.commit()
    return db_user

def create_address(db: Session, address: AddressCreate):
    db_address = Address(
        user_id=address.user_id,
        address=address.address,
        city=address.city,
        state=address.state,
        country=address.country,
        postal_code=address.postal_code,
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_user_addresses(db: Session, user_id: str):
    return db.query(Address).filter(Address.user_id == user_id).all()

def update_address(db: Session, address_id: int,user_id:str, address_update: AddressUpdate):
    #Ensure address belongs to the user
    db_address = db.query(Address).filter(Address.address_id == address_id, Address.user_id == user_id).first()
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if not db_address:
        return None

    if address_update.address:
        db_address.address = address_update.address
    if address_update.city:
        db_address.city = address_update.city
    if address_update.state:
        db_address.state = address_update.state
    if address_update.country:
        db_address.country = address_update.country
    if address_update.postal_code:
        db_address.postal_code = address_update.postal_code

    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int, user_id: str):
    # Ensure the address belongs to the user
    db_address = db.query(Address).filter(Address.address_id == address_id, Address.user_id == user_id).first()
    if not db_address:
        return HTTPException(status_code=404, detail="Address not found or does not belong to the user.")
    db_address = db.query(Address).filter(Address.address_id == address_id).first()
    if not db_address:
        return None

    db.delete(db_address)
    db.commit()
    return db_address