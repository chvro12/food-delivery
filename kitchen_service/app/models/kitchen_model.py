from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import uuid

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class KitchenOrder(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Génération automatique de l'ID
    order_id: str
    user_email: str
    items: List[OrderItem]
    status: str = "PENDING"  # Statut par défaut
    created_at: datetime = Field(default_factory=datetime.utcnow)
