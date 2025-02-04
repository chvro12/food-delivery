import jwt
from datetime import datetime, timedelta
from app.config.settings import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: int = 30):
    """ Crée un JWT avec une durée de vie définie """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """ Vérifie et décode le token JWT """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide
