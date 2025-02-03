import json
import bcrypt
from pathlib import Path
from app.models.user_model import User
from app.utils.jwt_utils import create_access_token

DB_FILE = Path("config/db.json")

def load_users():
    """ Charge les utilisateurs depuis le fichier JSON """
    if not DB_FILE.exists():
        return {"users": []}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_users(data):
    """ Sauvegarde les utilisateurs dans le fichier JSON """
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

def register_user(user: User):
    """ Enregistre un nouvel utilisateur """
    data = load_users()
    
    # Vérifier si l'utilisateur existe déjà
    if any(u["email"] == user.email for u in data["users"]):
        return {"error": "Email already registered"}
    
    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Ajouter le nouvel utilisateur
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": user.role
    }
    
    data["users"].append(new_user)
    save_users(data)
    
    return {"message": "User registered successfully"}

def login_user(user_login):
    """ Authentifie un utilisateur et génère un token """
    data = load_users()
    
    # Vérifier si l'utilisateur existe
    user = next((u for u in data["users"] if u["email"] == user_login.email), None)
    if not user or not bcrypt.checkpw(user_login.password.encode('utf-8'), user["password"].encode('utf-8')):
        return {"error": "Invalid email or password"}
    
    # Génération du token JWT
    token = create_access_token({"email": user["email"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

def get_users():
    """ Récupère la liste de tous les utilisateurs """
    data = load_users()
    return data["users"]

def update_user(email: str, updated_data: dict, current_user: dict):
    """ Met à jour un utilisateur """
    data = load_users()
    user_index = next((i for i, u in enumerate(data["users"]) if u["email"] == email), None)

    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Vérifier si l'utilisateur a le droit de modifier
    if current_user["email"] != email and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    # Mise à jour des données autorisées
    for key, value in updated_data.items():
        if key in ["username", "password"]:
            if key == "password":
                value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            data["users"][user_index][key] = value

    save_users(data)
    return {"message": "User updated successfully"}

def delete_user(email: str, current_user: dict):
    """ Supprime un utilisateur """
    data = load_users()
    user_index = next((i for i, u in enumerate(data["users"]) if u["email"] == email), None)

    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Seul un admin peut supprimer un compte
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")

    del data["users"][user_index]
    save_users(data)
    return {"message": "User deleted successfully"}
