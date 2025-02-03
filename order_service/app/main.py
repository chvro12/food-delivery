from fastapi import FastAPI
from app.routes.order_routes import router as order_router

app = FastAPI(title="Order Service API")

app.include_router(order_router)

@app.get("/")
def root():
    return {"message": "Order Service is Running!"}
