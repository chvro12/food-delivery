from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KitchenOrder(BaseModel):
    order_id: str
    status: str
    notes: Optional[str] = None
    items: List[str]
    created_at: datetime = None

class StatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None