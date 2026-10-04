from pydantic import BaseModel
from typing import Dict, Any

class ProductBase(BaseModel):
    title: str
    category: str
    description: str | None = None
    price: float
    inventory: int
    specifications: Dict[str, Any] | None = None  # Словарь для характеристик

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
