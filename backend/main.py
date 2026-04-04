from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import engine, get_db
import models
from models import Product
from schemas import ProductCreate, ProductUpdate, ProductResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Low Stock Alert Tracker API")

@app.get("/api/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """Get all tracked products"""
    products = db.query(Product).all()
    return products

@app.post("/api/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to track"""
    db_product = Product(
        name=product.name,
        quantity=product.quantity,
        threshold=product.threshold
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update product quantity"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    
    db_product.quantity = product.quantity
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
