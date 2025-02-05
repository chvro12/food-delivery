from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import User, UserLogin
from app.services.user_service import register_user, login_user, get_users, update_user, delete_user
from app.middlewares.auth_middleware import get_current_user, check_role

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: User):
    """ Inscription d'un nouvel utilisateur """
    return register_user(user)


@router.post("/login")
async def login(user: UserLogin):
    """ Connexion et génération du token JWT """
    return login_user(user)


@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_user)):
    """ Accessible à tous les utilisateurs connectés """
    return {"message": "Welcome!", "current_user": current_user}


@router.get("/admin/users")
async def get_all_users(current_user: dict = Depends(check_role("admin"))):
    """ Accessible uniquement aux admins """
    return get_users()


@router.put("/users/{email}")
async def update_user_route(email: str, updated_data: dict, current_user: dict = Depends(get_current_user)):
    """ Met à jour un utilisateur (lui-même ou admin) """
    return update_user(email, updated_data, current_user)


@router.delete("/users/{email}")
async def delete_user_route(email: str, current_user: dict = Depends(check_role("admin"))):
    """ Supprime un utilisateur (uniquement par admin) """
    return delete_user(email, current_user)
