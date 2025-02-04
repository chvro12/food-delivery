from fastapi import APIRouter, Header, HTTPException
from app.models.kitchen_model import StatusUpdate, KitchenOrder
from app.services.kitchen_service import get_kitchen_orders, update_kitchen_order_status, add_kitchen_order
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/orders")
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

@router.post("/orders")
async def create_kitchen_order(
   order_data: dict,
   authorization: str = Header(None),
   x_user_email: str = Header(None, alias="X-User-Email"), 
   x_user_role: str = Header(None, alias="X-User-Role")
):
   if x_user_role != "chef":
       raise HTTPException(status_code=403, detail="Access denied. ['chef'] role required.")

   logger.info(f"Creating kitchen order: {order_data}")
   new_order = add_kitchen_order(order_data)
   
   return {
       "status": "success",
       "message": "Order created in kitchen",
       "order": new_order
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