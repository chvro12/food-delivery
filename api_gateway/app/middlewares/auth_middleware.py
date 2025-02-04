from fastapi import Request, HTTPException, Header
from jose import JWTError, jwt
from app.utils.jwt_utils import verify_token

async def auth_middleware(request: Request, authorization: str = Header(None)):
    """Middleware unifié pour la vérification des tokens"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        # Vérification du token
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Stockage des informations utilisateur
        request.state.user = payload
        request.state.token = token  # Stockage du token original
        request.state.user_email = payload.get("email")
        request.state.user_role = payload.get("role")
        
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")