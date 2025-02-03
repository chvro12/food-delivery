from fastapi import APIRouter, Depends, HTTPException
from app.models.delivery_model import DeliveryOrder
from app.services.delivery_service import get_delivery_orders, add_delivery_order, update_delivery_order_status
from app.middlewares.auth_middleware import get_current_user, check_role

router = APIRouter()

@router.get("/orders", dependencies=[Depends(check_role(["livreur", "admin"]))])
async def list_deliveries():
    """ Liste toutes les livraisons """
    return get_delivery_orders()

@router.post("/orders", dependencies=[Depends(check_role(["chef"]))])
async def create_delivery_order(order: DeliveryOrder):
    """ Permet aux chefs d'ajouter une commande prête pour la livraison """
    return add_delivery_order(order.dict())

@router.put("/orders/{order_id}/status", dependencies=[Depends(check_role(["livreur"]))])
async def change_delivery_status(order_id: str, status: str):
    """ Met à jour le statut d'une commande en livraison """
    updated_order = update_delivery_order_status(order_id, status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return updated_order
