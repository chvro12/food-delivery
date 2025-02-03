from fastapi import APIRouter, Depends, HTTPException
from app.models.order_model import Order
from app.services.order_service import create_order, get_orders, get_order_by_id, update_order_status
from app.middlewares.auth_middleware import get_current_user, check_role

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", dependencies=[Depends(check_role(["client"]))])
async def place_order(order: Order, current_user: dict = Depends(get_current_user)):
    """ Permet aux clients de passer une commande """
    return create_order(order)

@router.get("/", dependencies=[Depends(check_role(["chef", "livreur", "admin"]))])
async def list_orders(current_user: dict = Depends(get_current_user)):  
    """ Liste toutes les commandes """
    return get_orders()

@router.get("/{order_id}")
async def get_order(order_id: str, current_user: dict = Depends(get_current_user)):
    """ Récupère une commande spécifique """
    order = get_order_by_id(order_id)
    
    if current_user["role"] == "client" and order["user_email"] != current_user["email"]:
        raise HTTPException(status_code=403, detail="Access denied. You can only view your own orders.")
    
    return order

@router.put("/{order_id}/status", dependencies=[Depends(check_role(["chef", "livreur"]))])
async def change_order_status(order_id: str, status: str, current_user: dict = Depends(get_current_user)):
    """ Met à jour le statut d'une commande avec restrictions par rôle """
    return update_order_status(order_id, status)
