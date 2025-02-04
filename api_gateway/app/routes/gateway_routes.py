from fastapi import APIRouter, Request, Depends, Security
from app.services.gateway_service import call_auth_service, call_order_service, call_kitchen_service, call_delivery_service
from app.middlewares.auth_middleware import get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

### ✅ ROUTAGE AUTHENTIFICATION VIA API GATEWAY ###


@router.post("/auth/login")
async def login(data: dict):
    """ Route pour l'authentification via API Gateway """
    return await call_auth_service("auth/login", method="POST", data=data)


@router.get("/auth/users")
async def get_users(token: str = Security(oauth2_scheme), user: dict = Depends(get_current_user)):
    """ Vérifie l'utilisateur et retourne ses infos """
    return await call_auth_service("auth/users", headers={"Authorization": f"Bearer {token}"})


### ORDER SERVICE ###
@router.post("/order/orders")
async def create_order(request: Request, token: str = Security(oauth2_scheme), user: dict = Depends(get_current_user)):
    data = await request.json()
    return await call_order_service("orders", headers={"Authorization": f"Bearer {token}"}, method="POST", data=data)


@router.get("/order/orders")
async def get_orders(token: str = Security(oauth2_scheme), user: dict = Depends(get_current_user)):
    return await call_order_service("orders", headers={"Authorization": f"Bearer {token}"})

### KITCHEN SERVICE ###


@router.get("/kitchen/orders")
async def get_kitchen_orders(token: str = Security(oauth2_scheme), user: dict = Depends(get_current_user)):
    return await call_kitchen_service("kitchen/orders", headers={"Authorization": f"Bearer {token}"})

### DELIVERY SERVICE ###


@router.get("/delivery/orders")
async def get_delivery_orders(token: str = Security(oauth2_scheme), user: dict = Depends(get_current_user)):
    return await call_delivery_service("delivery/orders", headers={"Authorization": f"Bearer {token}"})
