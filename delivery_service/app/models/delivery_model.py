from pydantic import BaseModel
from typing import List
from datetime import datetime

class DeliveryItem(BaseModel):
    name: str
    quantity: int
    price: float

class DeliveryOrder(BaseModel):
    id: str
    order_id: str
    user_email: str
    items: List[DeliveryItem]
    status: str = "PENDING"
    created_at: datetime = datetime.utcnow()
