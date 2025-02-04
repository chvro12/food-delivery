import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt_utils import verify_token
from ..utils.jwt_utils import verify_token  # ✅ Utilisation de l'import relatif
from app.config.settings import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """ Middleware pour extraire l'utilisateur du token JWT """
    print(
        f"🔍 API Gateway - Vérification du token reçu: {token}")  # ✅ Ajoute ce log pour debug
    payload = verify_token(token)

    if payload is None:
        print("⛔ API Gateway - Token invalide !")  # ✅ Debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"✅ API Gateway - Token valide: {payload}")  # ✅ Debug
    return payload
