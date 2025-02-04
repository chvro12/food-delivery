from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.kitchen_routes import router as kitchen_router

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes avec un préfixe
app.include_router(kitchen_router, prefix="/kitchen")

@app.get("/")
async def root():
    return {"message": "Kitchen Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}