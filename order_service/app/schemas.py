from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderResponse(OrderCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
