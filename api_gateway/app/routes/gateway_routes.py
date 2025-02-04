# app/routes/gateway_routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from app.middlewares.auth_middleware import auth_middleware
from app.services.gateway_service import (
    call_auth_service,
    call_order_service,
    call_kitchen_service,
    call_delivery_service
)

router = APIRouter()

### Routes Auth Service ###
@router.post("/auth/login")
async def login(credentials: dict):
    """Route de login"""
    try:
        return await call_auth_service(
            endpoint="auth/login",
            method="POST",
            data=credentials
        )
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/register")
async def register(user_data: dict):
    """Route d'enregistrement"""
    try:
        return await call_auth_service(
            endpoint="auth/register",
            method="POST",
            data=user_data
        )
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

### Routes Order Service ###
@router.post("/order/orders")
async def create_order(order_data: dict, request: Request, user: dict = Depends(auth_middleware)):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        return await call_order_service("orders", headers=headers, method="POST", data=order_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Nouvelle route pour obtenir une commande spécifique
@router.get("/order/orders/{order_id}")
async def get_order(order_id: int, request: Request, user: dict = Depends(auth_middleware)):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        return await call_order_service(f"orders/{order_id}", headers=headers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour mettre à jour une commande
@router.put("/order/orders/{order_id}")
async def update_order(
    order_id: int,
    order_data: dict,
    request: Request,
    user: dict = Depends(auth_middleware)
):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        return await call_order_service(
            f"orders/{order_id}",
            headers=headers,
            method="PUT",
            data=order_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour supprimer une commande
@router.delete("/order/orders/{order_id}")
async def delete_order(
    order_id: int,
    request: Request,
    user: dict = Depends(auth_middleware)
):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        return await call_order_service(
            f"orders/{order_id}",
            headers=headers,
            method="DELETE"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
### Routes Admin ###
@router.get("/auth/users")
async def get_users(request: Request, user: dict = Depends(auth_middleware)):
    """Liste des utilisateurs (admin)"""
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
        }
        return await call_auth_service("auth/users", headers=headers)
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kitchen/orders")
async def get_kitchen_orders(request: Request, user: dict = Depends(auth_middleware)):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        print(f"Calling kitchen service - headers: {headers}")  # Debug log
        return await call_kitchen_service(
            endpoint="kitchen/orders",  # Vérifiez que cet endpoint correspond à votre Kitchen Service
            headers=headers
        )
    except Exception as e:
        print(f"Error getting kitchen orders: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/kitchen/orders/{order_id}/status")
async def update_kitchen_status(
    order_id: str,
    status_data: dict,
    request: Request,
    user: dict = Depends(auth_middleware)
):
    try:
        headers = {
            "Authorization": f"Bearer {request.state.token}",
            "X-User-Email": request.state.user_email,
            "X-User-Role": request.state.user_role
        }
        print(f"Updating kitchen order {order_id} with data: {status_data}")  # Debug log
        return await call_kitchen_service(
            endpoint=f"kitchen/orders/{order_id}/status",
            method="PUT",
            headers=headers,
            data=status_data
        )
    except Exception as e:
        print(f"Error updating kitchen status: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))