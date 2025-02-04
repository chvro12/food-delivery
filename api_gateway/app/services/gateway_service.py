import httpx
from fastapi import HTTPException
from app.config.settings import AUTH_SERVICE_URL, ORDER_SERVICE_URL, KITCHEN_SERVICE_URL, DELIVERY_SERVICE_URL


async def call_service(service_url: str, endpoint: str, headers: dict = None, method: str = 'GET', data: dict = None):
    """
    Appelle un service spécifique (Auth, Order, Kitchen, Delivery) via API Gateway.
    """
    url = f"{service_url}/{endpoint}"

    print(f"🔄 [API Gateway] Envoi de requête {method} à {url}")  # Debug log

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, json=data)

            # Debug log
            print(
                f"✅ [API Gateway] Réponse {response.status_code} : {response.text}")

            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        # Debug log
        print(
            f"⛔ [API Gateway] Erreur HTTP {exc.response.status_code} : {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code,
                            detail=f"Error: {exc.response.text}")
    except Exception as e:
        print(f"❌ [API Gateway] Erreur de connexion : {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500, detail=f"Error connecting to service: {str(e)}")

# 🔗 Spécificités par service


async def call_auth_service(endpoint: str, headers: dict = None, method: str = 'GET', data: dict = None):
    return await call_service(AUTH_SERVICE_URL, endpoint, headers, method, data)


async def call_order_service(endpoint: str, headers: dict = None, method: str = 'GET', data: dict = None):
    return await call_service(ORDER_SERVICE_URL, endpoint, headers, method, data)


async def call_kitchen_service(endpoint: str, headers: dict = None, method: str = 'GET', data: dict = None):
    return await call_service(KITCHEN_SERVICE_URL, endpoint, headers, method, data)


async def call_delivery_service(endpoint: str, headers: dict = None, method: str = 'GET', data: dict = None):
    return await call_service(DELIVERY_SERVICE_URL, endpoint, headers, method, data)
