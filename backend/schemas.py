from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., ge=0)
    threshold: int = Field(..., ge=0)
    max_quantity: int = Field(..., ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    quantity: int = Field(..., ge=0)


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
