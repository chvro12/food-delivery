from fastapi import FastAPI
from app.routes.delivery_routes import router as delivery_router

app = FastAPI()

# Inclusion des routes de livraison
app.include_router(delivery_router, prefix="/delivery")

@app.get("/")
def read_root():
    return {"message": "Delivery Service is running"}
