from fastapi import APIRouter, Depends, HTTPException
from app.services.kitchen_service import get_kitchen_orders, add_kitchen_order, update_kitchen_order_status
from app.middlewares.auth_middleware import get_current_user, check_role
from app.models.kitchen_model import KitchenOrder

router = APIRouter()

# 👨‍🍳 **Seuls les chefs peuvent voir toutes les commandes en cuisine**
@router.get("/orders", dependencies=[Depends(check_role(["chef"]))])
async def list_kitchen_orders():
    """ Liste toutes les commandes en cuisine """
    return get_kitchen_orders()


# 🛒 **Ajouter une commande en cuisine**
@router.post("/orders", dependencies=[Depends(check_role(["chef"]))])
async def add_order_to_kitchen(order: KitchenOrder, current_user: dict = Depends(get_current_user)):
    """ Ajouter une commande en cuisine """
    return add_kitchen_order(order.dict())


# 🔄 **Mettre à jour le statut d'une commande en cuisine**
@router.put("/orders/{order_id}/status", dependencies=[Depends(check_role(["chef"]))])
async def change_kitchen_order_status(order_id: str, status: str, current_user: dict = Depends(get_current_user)):
    """ Met à jour le statut d'une commande en cuisine """

    valid_statuses = ["PENDING", "PREPARING", "READY"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {valid_statuses}")

    updated_order = update_kitchen_order_status(order_id, status)
    if updated_order:
        return {"message": f"Kitchen order {order_id} updated to {status}"}
    
    raise HTTPException(status_code=404, detail="Order not found")
