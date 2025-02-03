from fastapi import APIRouter, Depends, Request, HTTPException, Header
from app.services.gateway_service import call_auth_service, call_order_service, call_kitchen_service, call_delivery_service
from app.middlewares.auth_middleware import get_current_user

router = APIRouter()

### 🔑 AUTH SERVICE ###
@router.post("/auth/login")
async def login(data: dict):
    """Redirige la connexion vers Auth Service"""
    return await call_auth_service("auth/login", method="POST", data=data)

### 🛒 ORDER SERVICE ###
@router.post("/orders")
async def create_order(request: Request, user: dict = Depends(get_current_user)):
    """Créer une commande"""
    data = await request.json()
    return await call_order_service("orders", method="POST", data=data, headers={"Authorization": f"Bearer {user['token']}"})

@router.get("/orders")
async def get_orders(user: dict = Depends(get_current_user)):
    """Récupérer les commandes"""
    return await call_order_service("orders", headers={"Authorization": f"Bearer {user['token']}"})

### 🍽 KITCHEN SERVICE ###
@router.post("/kitchen/orders")
async def create_kitchen_order(request: Request, user: dict = Depends(get_current_user)):
    """Créer une commande de cuisine"""
    data = await request.json()
    return await call_kitchen_service("orders", method="POST", data=data, headers={"Authorization": f"Bearer {user['token']}"})

### 🚚 DELIVERY SERVICE ###
@router.post("/delivery/orders")
async def create_delivery_order(request: Request, user: dict = Depends(get_current_user)):
    """Créer une livraison"""
    data = await request.json()
    return await call_delivery_service("orders", method="POST", data=data, headers={"Authorization": f"Bearer {user['token']}"})

@router.post("/order/orders")
async def create_order(request: Request, user: dict = Depends(get_current_user)):
    data = await request.json()
    return await call_order_service("orders", headers={"Authorization": f"Bearer {user['token']}"}, method="POST", data=data)
