import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://127.0.0.1:8000")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://127.0.0.1:8001")
KITCHEN_SERVICE_URL = os.getenv("KITCHEN_SERVICE_URL", "http://127.0.0.1:8002")
DELIVERY_SERVICE_URL = os.getenv("DELIVERY_SERVICE_URL", "http://127.0.0.1:8003")
