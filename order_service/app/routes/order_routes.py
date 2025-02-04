from fastapi import APIRouter, Depends, HTTPException, Header
from app.utils.jwt_utils import verify_token

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_token(authorization: str = Header(None)):
    """ Extrait et valide le token JWT depuis l'en-tête Authorization """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    return authorization.split("Bearer ")[1]  # Retourne uniquement le token


@router.post("/")
async def create_order(order_data: dict, token: str = Depends(get_token)):
    """ Création d'une commande après validation du token """
    print(f"🔍 [Order Service] Token reçu : {token}")  # Debug log

    user = verify_token(token)
    if user is None:
        print("⛔ [Order Service] Token invalide !")  # Debug log
        raise HTTPException(status_code=401, detail="Invalid token")

    print(f"✅ [Order Service] Utilisateur validé : {user}")  # Debug log
    return {"message": "Commande créée avec succès", "user": user, "order_data": order_data}


@router.get("/")
async def list_orders(token: str = Depends(get_token)):
    """ Récupère la liste des commandes après validation du token """
    print(
        f"🔍 [Order Service] Vérification du token pour récupération des commandes : {token}")  # Debug log

    user = verify_token(token)
    if user is None:
        # Debug log
        print(
            "⛔ [Order Service] Token invalide lors de la récupération des commandes !")
        raise HTTPException(status_code=401, detail="Invalid token")

    print(f"✅ [Order Service] Utilisateur validé : {user}")  # Debug log
    return {"message": "Liste des commandes récupérée avec succès", "user": user}
