from sqlalchemy.orm import Session
from app.db.models import Order  # <-- Import your SQLAlchemy Order model
from app.schemas import OrderCreate, OrderUpdate
from fastapi import HTTPException
from app.crud.crud_products import get_product, update_product_stock  # <-- Import the function to check product existence

def create_order(db: Session, order: OrderCreate):
    #check if items in order exist and available
    product = get_product(db, product_id=order.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.count < order.quantity:
        raise HTTPException(status_code=400, detail="Insufficient product stock")
    stock_update = update_product_stock(db, product_id=order.product_id, quantity=order.quantity, operation="decrease")
    if not stock_update:
        raise HTTPException(status_code=400, detail="Failed to update product stock")
    db_order = Order(  # <-- Use SQLAlchemy model, not Pydantic
        user_id=order.user_id,
        product_id=order.product_id,
        payment_status=order.payment_status,
        address_id=order.address_id,
        quantity=order.quantity,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: str):
    return db.query(Order).filter(Order.order_id == order_id).first()

def update_order(db: Session, order_id: str, order_update: OrderUpdate):
    db_order = get_order_by_id(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_update.payment_status is not None:
        db_order.payment_status = order_update.payment_status
    if order_update.status is not None:
        db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: str):
    db_order = get_order_by_id(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    # Check if the order can be deleted based on its status
    db.delete(db_order)
    db.commit()
    return db_order

def get_orders_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 10):
    db_orders = db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return db_orders