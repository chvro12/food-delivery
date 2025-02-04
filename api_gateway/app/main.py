from fastapi import FastAPI
from app.routes.gateway_routes import router as gateway_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # A adapter selon vos besoins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(gateway_router)

@app.get("/health")
async def health_check():
    """Route de vérification de santé de l'API"""
    return {"status": "healthy"}