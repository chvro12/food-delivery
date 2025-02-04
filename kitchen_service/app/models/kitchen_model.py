from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class KitchenOrder(BaseModel):
    items: List[OrderItem]
    status: str = "pending"
    notes: Optional[str] = None

class StatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None