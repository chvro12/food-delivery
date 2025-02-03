import json
import uuid
from datetime import datetime
from pathlib import Path
from app.models.delivery_model import DeliveryOrder

DB_FILE = Path("config/db.json")

def load_delivery_orders():
    """ Charge les livraisons depuis `db.json` """
    if not DB_FILE.exists():
        return []  

    with open(DB_FILE, "r") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []  

def save_delivery_orders(orders):
    """ Sauvegarde les livraisons dans `db.json` """
    with open(DB_FILE, "w") as file:
        json.dump(orders, file, indent=4, default=str)

def get_delivery_orders():
    """ Récupère toutes les livraisons """
    return load_delivery_orders()

def add_delivery_order(order_data: dict):
    """ Ajoute une nouvelle livraison """
    orders = load_delivery_orders()

    new_order_data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        **order_data
    }

    orders.append(new_order_data)
    save_delivery_orders(orders)
    return new_order_data

def update_delivery_order_status(order_id: str, new_status: str):
    """ Met à jour le statut d'une livraison """
    orders = load_delivery_orders()
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            save_delivery_orders(orders)
            return order
    return None
