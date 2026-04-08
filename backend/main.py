from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from typing import List
import threading

from .database import engine, get_db
from . import models
from . import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pantry Tracker API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager for real-time updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()


def notify_clients():
    """Notify connected clients about data changes using a background thread."""
    import asyncio
    import threading
    
    def send_notification():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(manager.broadcast({"action": "refresh"}))
        finally:
            loop.close()
    
    thread = threading.Thread(target=send_notification)
    thread.daemon = True
    thread.start()


@app.get("/api/products", response_model=List[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    """Get all products with their quantity and threshold."""
    products = db.query(models.Product).all()
    return products


@app.get("/api/shopping-list", response_model=List[schemas.ProductResponse])
def get_shopping_list(db: Session = Depends(get_db)):
    """Get only products that are at or below threshold (critical items)."""
    products = db.query(models.Product).filter(
        models.Product.quantity <= models.Product.threshold
    ).all()
    return products


@app.post("/api/products", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the tracker."""
    db_product = models.Product(
        name=product.name,
        quantity=product.quantity,
        threshold=product.threshold,
        max_quantity=product.max_quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Notify connected clients
    notify_clients()
    return db_product


@app.delete("/api/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product from the tracker."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    # Notify connected clients
    notify_clients()
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
    if adjustment.quantity < 0:
        raise HTTPException(status_code=400, detail="Quantity cannot be negative")
    db_product.quantity = adjustment.quantity
    db.commit()
    db.refresh(db_product)
    # Notify connected clients
    notify_clients()
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
    # Notify connected clients
    notify_clients()
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
    # Notify connected clients
    notify_clients()
    return db_product


@app.post("/api/products/{product_id}/bought", response_model=schemas.ProductResponse)
def mark_as_bought(product_id: int, db: Session = Depends(get_db)):
    """Mark product as bought - reset quantity to max value."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.quantity = db_product.max_quantity
    db.commit()
    db.refresh(db_product)
    # Notify connected clients
    notify_clients()
    return db_product


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, wait for messages from client
            data = await websocket.receive_text()
            # Client can send ping/pong or other messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Serve static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
