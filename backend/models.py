from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    threshold = Column(Integer, nullable=False, default=1)
