import httpx
from fastapi import HTTPException
from app.config.settings import AUTH_SERVICE_URL, ORDER_SERVICE_URL, KITCHEN_SERVICE_URL, DELIVERY_SERVICE_URL

async def call_service(service_url: str, endpoint: str, method: str = 'GET', data: dict = None, headers: dict = None):
    """ Fonction générique pour appeler un microservice """
    url = f"{service_url}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Service error: {exc.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error contacting service: {str(e)}")

async def call_auth_service(endpoint: str, method: str = 'GET', data: dict = None, headers: dict = None):
    return await call_service(AUTH_SERVICE_URL, endpoint, method, data, headers)

async def call_order_service(endpoint: str, method: str = 'GET', data: dict = None, headers: dict = None):
    return await call_service(ORDER_SERVICE_URL, endpoint, method, data, headers)

async def call_kitchen_service(endpoint: str, method: str = 'GET', data: dict = None, headers: dict = None):
    return await call_service(KITCHEN_SERVICE_URL, endpoint, method, data, headers)

async def call_delivery_service(endpoint: str, method: str = 'GET', data: dict = None, headers: dict = None):
    return await call_service(DELIVERY_SERVICE_URL, endpoint, method, data, headers)
