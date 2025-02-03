import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_jwt_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DB_FILE = Path(os.getenv("DB_FILE", "app/config/db.json"))
