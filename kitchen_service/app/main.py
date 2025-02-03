from fastapi import FastAPI
from app.routes.kitchen_routes import router as kitchen_router

app = FastAPI()

# 🔥 Enregistrer les routes de KitchenService
app.include_router(kitchen_router, prefix="/kitchen", tags=["Kitchen"])

@app.get("/")
async def root():
    return {"message": "KitchenService is running!"}
