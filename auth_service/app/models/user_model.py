from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "client"  # Rôles possibles : client, chef, livreur

class UserLogin(BaseModel):
    email: EmailStr
    password: str
