import json
import uuid
from datetime import datetime
from pathlib import Path
from app.models.kitchen_model import KitchenOrder

DB_FILE = Path("config/db.json")

def load_kitchen_orders():
    if not DB_FILE.exists():
        DB_FILE.parent.mkdir(exist_ok=True)
        save_kitchen_orders([])
        return []
    
    with open(DB_FILE, "r") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def save_kitchen_orders(orders):
    DB_FILE.parent.mkdir(exist_ok=True)
    with open(DB_FILE, "w") as file:
        json.dump(orders, file, indent=4)

def get_kitchen_orders():
    return load_kitchen_orders()

def add_kitchen_order(order_data: dict):
    orders = load_kitchen_orders()
    new_order_data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        **order_data
    }
    orders.append(new_order_data)
    save_kitchen_orders(orders)
    return new_order_data

def update_kitchen_order_status(order_id: str, new_status: str):
    orders = load_kitchen_orders()
    for order in orders:
        if order["id"] == order_id:
            order["status"] = new_status
            save_kitchen_orders(orders)
            return order
    return None