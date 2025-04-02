# TP Neo4j - API RESTful avec Flask

Ce projet est une API RESTful développée en Python avec Flask et connectée à une base de données Neo4j grâce à py2neo. Elle gère des entités comme les utilisateurs, les posts, les commentaires, les relations d'amitiés et les likes.

## Structure du projet
```
app-neo4j/
├── app.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── routes/
    ├── __init__.py
    ├── user_routes.py
    ├── post_routes.py
    └── comment_routes.py
```

## Lancement du projet

### 1. Installer les dépendances
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Lancer Neo4j avec Docker
```bash
docker run --name neo4j -d \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j
```

### 3. Lancer l'API Flask
```bash
python app.py
```


## Tests des routes avec `curl`

### Utilisateurs
- **Créer un utilisateur**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

- **Voir tous les utilisateurs**
```bash
curl http://localhost:5000/users
```

- **Voir un utilisateur**
```bash
curl http://localhost:5000/users/<user_id>
```

- **Modifier un utilisateur**
```bash
curl -X PUT http://localhost:5000/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Update", "email": "alice@upd.com"}'
```

- **Supprimer un utilisateur**
```bash
curl -X DELETE http://localhost:5000/users/<user_id>
```

### Amitiés
- **Ajouter un ami**
```bash
curl -X POST http://localhost:5000/users/<user_id>/friends \
  -H "Content-Type: application/json" \
  -d '{"friend_id": "<friend_id>"}'
```

- **Voir les amis d'un utilisateur**
```bash
curl http://localhost:5000/users/<user_id>/friends
```

- **Vérifier si deux utilisateurs sont amis**
```bash
curl http://localhost:5000/users/<user_id>/friends/<friend_id>
```

- **Voir les amis en commun**
```bash
curl http://localhost:5000/users/<user_id>/mutual-friends/<other_id>
```

- **Supprimer un ami**
```bash
curl -X DELETE http://localhost:5000/users/<user_id>/friends/<friend_id>
```

### Commentaires
- **Ajouter un commentaire à un post**
```bash
curl -X POST http://localhost:5000/comments \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<user_id>", "post_id": "<post_id>", "content": "Commentaire ici"}'
```

- **Voir les commentaires d'un post**
```bash
curl http://localhost:5000/posts/<post_id>/comments
```

### Likes
- **Liker un post**
```bash
curl -X POST http://localhost:5000/posts/<post_id>/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<user_id>"}'
```

- **Unliker un post**
```bash
curl -X DELETE http://localhost:5000/posts/<post_id>/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": "<user_id>"}'
```


