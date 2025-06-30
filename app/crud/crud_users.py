from sqlalchemy.orm import Session
from app.db.models import User, Address
from app.schemas import UserCreate, UserUpdate, AddressCreate, AddressUpdate
from app.core.security import hash_password, verify_password


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
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

def delete_user(db: Session, user_email: str):
    db_user = get_user_by_email(db, email=user_email)
    if not db_user:
        return None

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