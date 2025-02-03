import json
import uuid
from pathlib import Path
from datetime import datetime
from fastapi import HTTPException
from app.models.order_model import Order
from app.config.settings import DB_FILE

def load_orders():
    """ Charge les commandes depuis le fichier JSON """
    if not DB_FILE.exists():
        return {"orders": []}
    with open(DB_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"orders": []}

def save_orders(data):
    """ Sauvegarde les commandes dans le fichier JSON """
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_order(order_data: Order):
    """ Crée une nouvelle commande """
    data = load_orders()
    
    order_id = str(uuid.uuid4())
    new_order = {
        "id": order_id,
        "user_email": order_data.user_email,
        "items": [item.dict() for item in order_data.items],
        "total_price": order_data.total_price,
        "status": "PENDING",
        "created_at": order_data.created_at.isoformat()
    }
    
    data["orders"].append(new_order)
    save_orders(data)

    return {"message": "Order created successfully", "order_id": order_id}

def get_orders():
    """ Récupère toutes les commandes """
    return load_orders()["orders"]

def get_order_by_id(order_id: str):
    """ Récupère une commande spécifique """
    data = load_orders()
    order = next((o for o in data["orders"] if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def update_order_status(order_id: str, status: str):
    """ Met à jour le statut d'une commande """
    data = load_orders()
    order_index = next((i for i, o in enumerate(data["orders"]) if o["id"] == order_id), None)

    if order_index is None:
        raise HTTPException(status_code=404, detail="Order not found")

    data["orders"][order_index]["status"] = status
    save_orders(data)

    return {"message": f"Order {order_id} updated to {status}"}
