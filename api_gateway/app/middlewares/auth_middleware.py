from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer
import jwt
from app.config.settings import SECRET_KEY, ALGORITHM

security = HTTPBearer()

async def get_current_user(request: Request, token: str = Security(security)):
    print("🔍 TOKEN REÇU:", token.credentials)  # DEBUG

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
