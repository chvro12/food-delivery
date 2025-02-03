from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router

app = FastAPI()

# Enregistrer les routes
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "Auth Service is running!"}
