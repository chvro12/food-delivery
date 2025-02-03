# 📘 Documentation du Système de Microservices

## 📌 Introduction

Ce document décrit l'architecture, la communication et l'intégration des microservices dans le projet **Food Delivery System**. Le projet repose sur **FastAPI** et suit une architecture **microservices** avec un **API Gateway** qui centralise la gestion des requêtes.

---

## 🏗️ **Architecture Globale**

Le projet est composé des microservices suivants :

1. **API Gateway** - Intermédiaire entre le client et les services.
2. **Auth Service** - Gère l'authentification et les rôles.
3. **Order Service** - Gère les commandes passées par les clients.
4. **Kitchen Service** - Gère la préparation des commandes.
5. **Delivery Service** - Gère la livraison des commandes.

### 📡 **Communication entre les Microservices**

- **L'API Gateway** est le point d'entrée unique pour toutes les requêtes.
- **Auth Service** génère et valide les tokens JWT.
- **Order Service** communique avec **Kitchen Service** et **Delivery Service** pour gérer le cycle de vie des commandes.
- Les microservices communiquent via des requêtes **HTTP** avec **httpx**.

---

## 🚀 **Démarrer chaque microservice**

### 📌 **Prérequis**

- Python 3.8+
- Virtualenv installé
- Dépendances installées (`pip install -r requirements.txt`)

### 🔄 **Lancer les microservices**

### **1️⃣ API Gateway**

```
cd api_gateway
uvicorn app.main:app --reload --port 8080
```

Accès : `http://127.0.0.1:8080/docs`

### **2️⃣ Auth Service** (Authentification)

```
cd auth_service
uvicorn app.main:app --reload --port 8000
```

Accès : `http://127.0.0.1:8000/docs`

### **3️⃣ Order Service** (Gestion des commandes)

```
cd order_service
uvicorn app.main:app --reload --port 8001
```

Accès : `http://127.0.0.1:8001/docs`

### **4️⃣ Kitchen Service** (Cuisine)

```
cd kitchen_service
uvicorn app.main:app --reload --port 8002
```

Accès : `http://127.0.0.1:8002/docs`

### **5️⃣ Delivery Service** (Livraison)

```
cd delivery_service
uvicorn app.main:app --reload --port 8003
```

Accès : `http://127.0.0.1:8003/docs`

---

## 🔑 **Auth Service** (Service d'Authentification)

### 📌 Rôles gérés :

- **Client** : Peut passer des commandes.
- **Chef** : Peut gérer les commandes en cuisine.
- **Livreur** : Peut mettre à jour le statut des livraisons.
- **Admin** : Peut voir toutes les commandes.

### 🔄 **Fonctionnalités :**

- **/auth/login** → Authentification et génération d’un token JWT.
- **Middleware** intégré pour sécuriser les autres services.

---

## 🛒 **Order Service** (Gestion des Commandes)

### 🔄 **Fonctionnalités :**

- **Créer une commande** (`POST /orders`)
- **Lister toutes les commandes** (`GET /orders`) (Accès : `chef`, `livreur`, `admin`)
- **Obtenir une commande spécifique** (`GET /orders/{order_id}`)
- **Modifier le statut d'une commande** (`PUT /orders/{order_id}/status`)

📌 **Une commande suit ces statuts :** `PENDING` → `PREPARING` → `READY` → `PICKED_UP` → `DELIVERED`

---

## 👨‍🍳 **Kitchen Service** (Gestion de la Cuisine)

### 🔄 **Fonctionnalités :**

- **Récupérer les commandes en attente** (`GET /kitchen/orders`)
- **Mettre à jour le statut** (`PUT /kitchen/orders/{order_id}/status`)

📌 **Statuts gérés :** `PREPARING`, `READY`

---

## 🚚 **Delivery Service** (Gestion des Livraisons)

### 🔄 **Fonctionnalités :**

- **Récupérer les commandes prêtes** (`GET /delivery/orders`)
- **Changer le statut** (`PUT /delivery/orders/{order_id}/status`)

📌 **Statuts gérés :** `PICKED_UP`, `DELIVERED`

---

## 🌍 **API Gateway** (Point d'Entrée Unique)

### 🔄 **Fonctionnement :**

- Redirige les requêtes vers les microservices correspondants.
- Vérifie l’authentification via **Auth Service**.
- Ajoute l’autorisation pour les opérations restreintes.

### **Exemples de requêtes :**

### 🔑 **Authentification**

```
curl -X POST 'http://127.0.0.1:8080/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email": "client@example.com", "password": "password123"}'
```

CHEF 

curl -X POST 'http://127.0.0.1:8080/auth/login' \
-H 'Content-Type: application/json' \
-d '{
"email": "[chef@example.com](mailto:chef@example.com)",
"password": "chefpassword"
}'

Livreur

curl -X POST 'http://127.0.0.1:8080/auth/login' \
-H 'Content-Type: application/json' \
-d '{
"email": "[livreur@example.com](mailto:livreur@example.com)",
"password": "livreurpassword"
}'

Admin 

curl -X POST 'http://127.0.0.1:8080/auth/login' \
-H 'Content-Type: application/json' \
-d '{
"email": "[admin@example.com](mailto:admin@example.com)",
"password": "adminpassword"
}'

### 🛒 **Passer une commande** (via API Gateway)

```
curl -X POST 'http://127.0.0.1:8080/order/orders' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{"user_email": "test@example.com", "items": [{"name": "Pizza", "quantity": 2, "price": 10.99}], "total_price": 21.98}'
```

### 🚚 **Mettre à jour le statut de la livraison**

```
curl -X PUT 'http://127.0.0.1:8080/delivery/orders/{order_id}/status' \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{"status": "PICKED_UP"}'
```

---

## 🛠️ **Technologies Utilisées**

- **FastAPI** (Framework web)
- **Uvicorn** (Serveur ASGI)
- **httpx** (Requêtes HTTP asynchrones)
- **JWT** (Authentification)
- **Docker** (Facultatif pour le déploiement)

---

