from pydantic import BaseModel, Field
from typing import Optional, List  
from app.schemas import ProductUpdate, ProductCreate, ProductRead, CategoryRead
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import create_access_token, decode_access_token, token_expired

router = APIRouter()
from app.db.session import get_db
from app.crud import crud_products
from sqlalchemy.orm import Session

@router.get("/categories", response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    """
    Retrieve a list of distinct product categories.
    """
    categories = crud_products.get_categories(db)
    return categories

@router.post("/categories", response_model=CategoryRead)
def create_category(category_name: str, db: Session = Depends(get_db)):
    """
    Create a new product category.
    """
    return crud_products.create_category(db=db, category_name=category_name)

@router.delete("/categories/{category_id}", response_model=CategoryRead)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    """
    Delete a product category.
    """
    return crud_products.delete_category(db=db, category_id=category_id)

@router.get("/products", response_model=List[ProductRead])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of products with pagination.
    """
    products = crud_products.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/products", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.
    """
    return crud_products.create_product(db=db, product=product)

@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single product by its ID.
    """
    product = crud_products.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: str, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update product details.
    """
    updated_product = crud_products.update_product(db=db, product_id=product_id, product_update=product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}", response_model=ProductRead)
def delete_product(product_id: str, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.
    """
    deleted_product = crud_products.delete_product(db=db, product_id=product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product