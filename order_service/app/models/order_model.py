from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    user_email: str
    items: List[OrderItem]
    total_price: float
    created_at: datetime = datetime.utcnow()
    status: str = "PENDING"
