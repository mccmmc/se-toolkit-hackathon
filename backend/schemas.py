from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    quantity: int
    threshold: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    quantity: int

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
