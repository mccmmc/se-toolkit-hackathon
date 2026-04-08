from sqlalchemy import Column, Integer, String
from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    threshold = Column(Integer, nullable=False, default=1)
    max_quantity = Column(Integer, nullable=False, default=0)
