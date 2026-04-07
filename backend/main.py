from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from . import models
from . import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pantry Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """Get all products with their quantity and threshold."""
    products = db.query(models.Product).all()
    return products


@app.post("/api/products", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the tracker."""
    db_product = models.Product(
        name=product.name,
        quantity=product.quantity,
        threshold=product.threshold,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/api/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from the tracker."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None


@app.post("/api/products/{product_id}/adjust", response_model=schemas.ProductResponse)
def adjust_quantity(
    product_id: int,
    adjustment: schemas.ProductUpdate,
    db: Session = Depends(get_db),
):
    """Adjust the quantity of a product (set to new value)."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.quantity = adjustment.quantity
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post("/api/products/{product_id}/increment", response_model=schemas.ProductResponse)
def increment_quantity(product_id: int, db: Session = Depends(get_db)):
    """Increase product quantity by 1."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.quantity += 1
    db.commit()
    db.refresh(db_product)
    return db_product


@app.post("/api/products/{product_id}/decrement", response_model=schemas.ProductResponse)
def decrement_quantity(product_id: int, db: Session = Depends(get_db)):
    """Decrease product quantity by 1 (minimum 0)."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity cannot go below 0")
    db_product.quantity -= 1
    db.commit()
    db.refresh(db_product)
    return db_product


# Serve static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
