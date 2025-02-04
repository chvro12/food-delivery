from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router  # ✅ Import du routeur

app = FastAPI()

# ✅ Inclure les routes d'authentification
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API is running"}
