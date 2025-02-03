rder Service
Le Order Service est un microservice dédié à la gestion des commandes pour une application de livraison de repas. Il permet aux utilisateurs de passer des commandes, aux chefs de les gérer, et aux livreurs de les livrer. Il fonctionne en coordination avec le Auth Service, l’API Gateway, et d’autres microservices.

⚙️ Technologies utilisées
Python 3.8+
FastAPI pour une API rapide et asynchrone.
JWT (PyJWT) pour la validation des utilisateurs et des permissions.
httpx pour la communication entre services.
dotenv pour la gestion des variables d'environnement.
JSON File Storage pour stocker temporairement les commandes.
🚀 Installation

Installer les dépendances :

pip install -r requirements.txt
Configurer les variables d’environnement
Créer un fichier .env à la racine du projet :

SECRET_KEY=super_secret_jwt_key
ALGORITHM=HS256
AUTH_SERVICE_URL=http://127.0.0.1:8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
DB_FILE=app/config/db.json
4️⃣ Lancer le serveur :

uvicorn app.main:app --reload --port 8001
Accéder à la documentation interactive :

Swagger UI : http://127.0.0.1:8001/docs
ReDoc : http://127.0.0.1:8001/redoc
🔑 Endpoints principaux
Méthode Endpoint Rôle Requis Description
POST /orders/ Client Passer une nouvelle commande
GET /orders/ Chef, Livreur, Admin Voir toutes les commandes
GET /orders/{order_id} Client (sa commande), Chef, Livreur, Admin Voir une commande spécifique
PUT /orders/{order_id}/status Chef, Livreur Mettre à jour le statut d'une commande
🏷️ Rôles et permissions
Client : Peut passer des commandes et consulter ses propres commandes.
Chef : Peut voir toutes les commandes et mettre à jour le statut à PREPARING ou READY.
Livreur : Peut voir toutes les commandes et mettre à jour le statut à PICKED_UP ou DELIVERED.
Admin : Peut voir toutes les commandes.
Les permissions sont vérifiées via le Auth Service, et les tokens JWT sont utilisés pour authentifier les utilisateurs.

🛠 Exemples de requêtes avec cURL
🔹 1. Passer une commande (Client)

curl -X 'POST' 'http://127.0.0.1:8001/orders/' \
-H "Authorization: Bearer VOTRE_ACCESS_TOKEN" \
-H 'Content-Type: application/json' \
-d '{
"user_email": "test@example.com",
"items": [
{"name": "Pizza", "quantity": 2, "price": 10.99},
{"name": "Salad", "quantity": 1, "price": 5.99}
],
"total_price": 27.97
}'
🔹 2. Voir toutes les commandes (Chef, Livreur, Admin)

curl -X 'GET' 'http://127.0.0.1:8001/orders/' \
-H "Authorization: Bearer VOTRE_ACCESS_TOKEN"
🔹 3. Voir une commande spécifique (Client = sa commande, Chef/Livreur/Admin = toutes)

curl -X 'GET' 'http://127.0.0.1:8001/orders/ORDER_ID' \
-H "Authorization: Bearer VOTRE_ACCESS_TOKEN"
🔹 4. Mettre à jour le statut d'une commande (Chef ou Livreur)

curl -X 'PUT' 'http://127.0.0.1:8001/orders/ORDER_ID/status' \
-H "Authorization: Bearer VOTRE_ACCESS_TOKEN" \
-H 'Content-Type: application/json' \
-d '{
"status": "PREPARING"
}'
📡 Intégration avec l'API Gateway
L’API Gateway agit comme un proxy et redirige les requêtes des clients vers order_service.
Exemple via API Gateway :

curl -X 'GET' 'http://127.0.0.1:8080/order/orders' \
-H "Authorization: Bearer VOTRE_ACCESS_TOKEN"
Si tout est bien configuré, API Gateway fera suivre la requête vers order_service.
