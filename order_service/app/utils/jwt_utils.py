from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_jwt_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

print(f"🔑 [Order Service] SECRET_KEY chargé : {SECRET_KEY}")  # Debug log


def create_access_token(data: dict):
    """ Génère un token JWT """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    print(f"✅ [Order Service] Token généré : {token}")  # Debug log
    return token


def verify_token(token: str):
    """ Vérifie et décode un token JWT """
    print(
        f"🛠️ [Order Service] Token reçu pour vérification : {token}")  # Debug log

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ [Order Service] Token valide : {payload}")  # Debug log
        return payload
    except JWTError as e:
        print(f"⛔ [Order Service] Token invalide : {str(e)}")  # Debug log
        return None
