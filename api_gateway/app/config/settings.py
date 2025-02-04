import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ✅ Vérifie bien cette valeur
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_jwt_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://127.0.0.1:8001")
KITCHEN_SERVICE_URL = os.getenv("KITCHEN_SERVICE_URL", "http://127.0.0.1:8002")
DELIVERY_SERVICE_URL = os.getenv(
    "DELIVERY_SERVICE_URL", "http://127.0.0.1:8003")

# ✅ Ajoute ce log temporairement pour voir si c'est bien chargé
print(f"🔍 API Gateway - SECRET_KEY: {SECRET_KEY}")
