import json
import uuid
from datetime import datetime
from pathlib import Path
from app.models.kitchen_model import KitchenOrder

DB_FILE = Path("config/db.json")


def load_kitchen_orders():
    """ Charge les commandes en cuisine depuis `db.json` """
    if not DB_FILE.exists():
        return []  # Retourne une liste vide si le fichier n'existe pas

    with open(DB_FILE, "r") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, list) else []  # Vérifie que c'est une liste
        except json.JSONDecodeError:
            return []  # Retourne une liste vide si le JSON est invalide


def save_kitchen_orders(orders):
    """ Sauvegarde les commandes en cuisine dans `db.json` """
    with open(DB_FILE, "w") as file:
        json.dump(orders, file, indent=4)


def get_kitchen_orders():
    """ Récupère toutes les commandes en cuisine """
    return load_kitchen_orders()


def add_kitchen_order(order_data: dict):
    """ Ajoute une commande en cuisine """
    orders = load_kitchen_orders()
    
    new_order_data = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow(),  # Ajout de la date actuelle
        **order_data
    }

    new_order = KitchenOrder(**new_order_data)
    new_order_dict = new_order.model_dump()  # Convertit en dict
    new_order_dict["created_at"] = new_order.created_at.isoformat()  # ✅ Correction

    orders.append(new_order_dict)
    save_kitchen_orders(orders)
    return new_order_dict


def update_kitchen_order_status(order_id: str, new_status: str):
    """ Met à jour le statut d'une commande en cuisine """
    orders = load_kitchen_orders()
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            save_kitchen_orders(orders)
            return order
    return None
