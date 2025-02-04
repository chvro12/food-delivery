from fastapi import APIRouter, Header, HTTPException
from app.models.kitchen_model import StatusUpdate
from app.services.kitchen_service import get_kitchen_orders, update_kitchen_order_status

router = APIRouter()

@router.get("/orders")  # Route pour /orders sans le préfixe kitchen
async def get_orders(
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    if x_user_role != "chef":
        raise HTTPException(status_code=403, detail="Access denied. ['chef'] role required.")
    
    orders = get_kitchen_orders()
    return {
        "status": "success",
        "orders": orders
    }

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    status_update: StatusUpdate,
    authorization: str = Header(None),
    x_user_email: str = Header(None, alias="X-User-Email"),
    x_user_role: str = Header(None, alias="X-User-Role")
):
    if x_user_role != "chef":
        raise HTTPException(status_code=403, detail="Access denied. ['chef'] role required.")
    
    updated_order = update_kitchen_order_status(order_id, status_update.status)
    if not updated_order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    
    return {
        "status": "success",
        "message": f"Order status updated to {status_update.status}",
        "order": updated_order
    }