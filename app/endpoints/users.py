from pydantic import BaseModel, Field
from typing import Optional, List  
from app.schemas import UserRead, AddressRead, UserCreate, UserUpdate,LoginUser, AddressCreate, AddressBase, AddressUpdate
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import create_access_token, decode_access_token, token_expired

router = APIRouter()
from app.db.session import get_db
from app.crud import crud_users
from sqlalchemy.orm import Session

@router.get("/users", response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of users with pagination.
    """
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/register", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    existing_user = crud_users.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud_users.create_user(db=db, user=user)

class UserLoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_email: str = Field(..., description="Email of the logged-in user")

@router.post("/login", response_model=UserLoginResponse)
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    """
    Login a user and return user details.
    """
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if not db_user or not crud_users.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    # Generate access token 
    access_token = create_access_token(data={"email": db_user.email, "user_id": db_user.user_id})
    user_email = db_user.email
    return UserLoginResponse(access_token=access_token, token_type="bearer", user_email=user_email)

@router.patch("/users/{user_id}", response_model=UserRead)
def update_user(user: LoginUser, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user details.
    """
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud_users.update_user(db=db, user_email=user.email, user_update=user_update)
    return updated_user

@router.delete("/delete/{email}", response_model=UserRead)
def delete_user(email: str, db: Session = Depends(get_db)):
    """
    Delete a user by email.
    """
    db_user = crud_users.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    crud_users.delete_user(db=db, user_email=email)
    return db_user

@router.get("/addresses", response_model=List[AddressRead])
def get_user_addresses(access_token: str, db: Session = Depends(get_db)):
    """
    Get all addresses for a specific user.
    """
    expired = token_expired(access_token)
    if expired:
        raise HTTPException(status_code=401, detail="Access token has expired")
    user_id = decode_access_token(access_token).get("user_id")
    addresses = crud_users.get_user_addresses(db, user_id=user_id)
    if not addresses:
        raise HTTPException(status_code=404, detail="Addresses not found")
    return addresses

@router.post("/addresses", response_model=AddressRead)
def create_address(address: AddressBase, access_token: str, db: Session = Depends(get_db)):
    """
    Create a new address for the user.
    """
    expired = token_expired(access_token)
    if expired:
        raise HTTPException(status_code=401, detail="Access token has expired")
    user_id = decode_access_token(access_token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")
    address = AddressCreate(
        address=address.address,
        city=address.city,
        state=address.state,
        country=address.country,
        postal_code=address.postal_code,
        user_id=user_id
    )
    return crud_users.create_address(db=db, address=address)

@router.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: str, address_update: AddressUpdate, access_token: str, db: Session = Depends(get_db)):
    """
    Update an existing address.
    """
    expired = token_expired(access_token)
    if expired:
        raise HTTPException(status_code=401, detail="Access token has expired") 
    user_id = decode_access_token(access_token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")

    updated_address = crud_users.update_address(db=db, address_id=address_id,user_id=user_id, address_update=address_update)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return updated_address

@router.delete("/addresses/{address_id}", response_model=AddressRead)
def delete_address(address_id: str, access_token: str, db: Session = Depends(get_db)):
    """
    Delete an address by ID.
    """
    expired = token_expired(access_token)
    if expired:
        raise HTTPException(status_code=401, detail="Access token has expired")
    user_id = decode_access_token(access_token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")

    deleted_address = crud_users.delete_address(db=db, address_id=address_id, user_id=user_id)
    if isinstance(deleted_address, HTTPException):
        raise deleted_address
    if not deleted_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return deleted_address

@router.get("/addresses/{address_id}", response_model=AddressRead)
def get_address_by_id(address_id: str, access_token: str, db: Session = Depends(get_db)):
    """
    Get an address by its ID.
    """
    user_id = decode_access_token(access_token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid access token")

    address = crud_users.get_address_by_id(db=db, address_id=address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return address