from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Définition du routeur sans préfixe
router = APIRouter()

# Modèle de données pour les commandes
class OrderRequest(BaseModel):
    items: List[str]
    total: float
    status: Optional[str] = "pending"

# Routes
@router.get("/orders")
async def get_orders(
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    """Liste des commandes"""
    logger.info(f"Getting orders for user: {x_user_email}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    orders = [
        {"id": 1, "status": "pending", "items": ["Pizza"], "total": 15.00},
        {"id": 2, "status": "completed", "items": ["Burger"], "total": 12.00}
    ]
    
    return {
        "status": "success",
        "message": "Orders retrieved successfully",
        "user_email": x_user_email,
        "orders": orders
    }

@router.post("/orders")
async def create_order(
    order: OrderRequest,
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    """Création d'une commande"""
    logger.info(f"Creating order: {order.dict()} for user: {x_user_email}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    new_order = {
        "id": 1,  # Dans un vrai service, cet ID serait généré
        "items": order.items,
        "total": order.total,
        "status": order.status,
        "user_email": x_user_email
    }
    
    return {
        "status": "success",
        "message": "Order created successfully",
        "order": new_order
    }

@router.get("/orders/{order_id}")
async def get_order(
    order_id: int,
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    """Récupération d'une commande spécifique"""
    logger.info(f"Getting order {order_id} for user: {x_user_email}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    order = {
        "id": order_id,
        "status": "pending",
        "items": ["Pizza"],
        "total": 15.00,
        "user_email": x_user_email
    }
    
    return {
        "status": "success",
        "message": "Order retrieved successfully",
        "order": order
    }

@router.put("/orders/{order_id}")
async def update_order(
    order_id: int,
    order: OrderRequest,
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    """Mise à jour d'une commande"""
    logger.info(f"Updating order {order_id} for user: {x_user_email}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    updated_order = {
        "id": order_id,
        "items": order.items,
        "total": order.total,
        "status": order.status,
        "user_email": x_user_email
    }
    
    return {
        "status": "success",
        "message": "Order updated successfully",
        "order": updated_order
    }

@router.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    """Suppression d'une commande (admin uniquement)"""
    logger.info(f"Deleting order {order_id} for user: {x_user_email}")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if x_user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete orders")
        
    return {
        "status": "success",
        "message": f"Order {order_id} deleted successfully"
    }