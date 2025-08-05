from sqlalchemy.orm import Session
from app.db.models import Product, Category
from app.schemas import ProductBase, ProductCreate, ProductRead, ProductUpdate
from app.core.security import hash_password, verify_password
import re
from fastapi import HTTPException

def get_categories(db: Session) -> list[dict]:
    """
    Retrieve a list of distinct product categories.
    """
    # categories = db.query(Category.category).distinct().all()
    # return [category[0] for category in categories]
    #returns all categories without duplicates with id
    categories = db.query(Category).distinct().all()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return [{"id": category.category_id, "name": category.category} for category in categories]

def create_category(db: Session, category_name: str):
    """
    Create a new product category.
    """
    if not category_name:
        raise HTTPException(status_code=400, detail="Category name cannot be empty")
    
    existing_category = db.query(Category).filter(Category.category == category_name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(category=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def delete_category(db: Session, category_id: str):
    """
    Delete a product category.
    """
    category = db.query(Category).filter(Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return category



def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,  # <-- must match schema and model
        count=product.count,
        product_metadata=product.product_metadata
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: str) -> ProductRead:
    return db.query(Product).filter(Product.product_id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10) -> list[ProductRead]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: str, product_update: ProductUpdate) -> ProductRead:
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_stock(db: Session, product_id: str, quantity: int, operation: str) -> ProductRead:
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if operation == "decrease":
        if db_product.count < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
    if operation == "increase":
        db_product.count = str(int(db_product.count) + int(quantity))
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: str) -> ProductRead:
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product