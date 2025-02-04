from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.order_routes import router as order_router
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Ajouter CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(order_router)

# Route de test
@app.get("/")
async def root():
    return {"message": "Order Service is running"}

# Route de santé
@app.get("/health")
async def health_check():
    return {"status": "healthy"}