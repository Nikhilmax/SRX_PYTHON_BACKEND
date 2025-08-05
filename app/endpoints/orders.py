from pydantic import BaseModel, Field
from typing import Optional, List  
from app.schemas import OrderBase, OrderCreate, OrderRead, OrderUpdate
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import create_access_token, decode_access_token, token_expired

router = APIRouter()
from app.db.session import get_db
from app.crud import crud_orders
from sqlalchemy.orm import Session

@router.post("/orders", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    """
    return crud_orders.create_order(db=db, order=order)

@router.get("/orders", response_model=List[OrderRead])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of orders with pagination.
    """
    orders = crud_orders.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single order by its ID.
    """
    order = crud_orders.get_order_by_id(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: str, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """
    Update order details.
    """
    updated_order = crud_orders.update_order(db=db, order_id=order_id, order_update=order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/orders/{order_id}", response_model=OrderRead)
def delete_order(order_id: str, db: Session = Depends(get_db)):
    """
    Delete an order by its ID.
    """
    deleted_order = crud_orders.delete_order(db=db, order_id=order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

@router.get("/orders/user/{user_id}", response_model=List[OrderRead])
def get_orders_by_user(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve orders for a specific user with pagination.
    """
    orders = crud_orders.get_orders_by_user(db, user_id=user_id)
    return orders

