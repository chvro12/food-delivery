from fastapi import FastAPI
from app.routes.gateway_routes import router as gateway_router

app = FastAPI(title="API Gateway")

app.include_router(gateway_router)
