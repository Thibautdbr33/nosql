from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

user_routes = Blueprint('user_routes', __name__)

# Créer un utilisateur
@user_routes.route('/users', methods=['POST'])
def create_user():
    graph = current_app.graph
    data = request.get_json()
    user_id = str(uuid.uuid4())
    query = """
    CREATE (u:User {
        id: $id,
        name: $name,
        email: $email,
        created_at: $created_at
    }) RETURN u
    """
    result = graph.run(query, 
                       id=user_id,
                       name=data['name'],
                       email=data['email'],
                       created_at=str(datetime.utcnow())).data()
    return jsonify(result), 201

# Obtenir tous les utilisateurs
@user_routes.route('/users', methods=['GET'])
def get_users():
    graph = current_app.graph
    result = graph.run("MATCH (u:User) RETURN u").data()
    return jsonify(result)

# Obtenir un utilisateur par ID
@user_routes.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    graph = current_app.graph
    result = graph.run("MATCH (u:User {id: $id}) RETURN u", id=user_id).data()
    return jsonify(result[0]) if result else ('User not found', 404)

# Mettre à jour un utilisateur
@user_routes.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    graph = current_app.graph
    data = request.get_json()
    query = """
    MATCH (u:User {id: $id})
    SET u.name = $name, u.email = $email
    RETURN u
    """
    result = graph.run(query, id=user_id, name=data['name'], email=data['email']).data()
    return jsonify(result)

# Supprimer un utilisateur
@user_routes.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    graph = current_app.graph
    query = "MATCH (u:User {id: $id}) DETACH DELETE u"
    graph.run(query, id=user_id)
    return '', 204

# Ajouter un ami
@user_routes.route('/users/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    graph = current_app.graph
    data = request.get_json()
    friend_id = data['friend_id']
    query = """
    MATCH (u1:User {id: $user_id}), (u2:User {id: $friend_id})
    MERGE (u1)-[:FRIENDS_WITH]-(u2)
    """
    graph.run(query, user_id=user_id, friend_id=friend_id)
    return '', 204

# Supprimer un ami
@user_routes.route('/users/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    graph = current_app.graph
    query = """
    MATCH (u1:User {id: $user_id})-[f:FRIENDS_WITH]-(u2:User {id: $friend_id})
    DELETE f
    """
    graph.run(query, user_id=user_id, friend_id=friend_id)
    return '', 204

# Voir si deux utilisateurs sont amis
@user_routes.route('/users/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    graph = current_app.graph
    query = """
    MATCH (u1:User {id: $user_id})-[f:FRIENDS_WITH]-(u2:User {id: $friend_id})
    RETURN count(f) > 0 AS are_friends
    """
    result = graph.run(query, user_id=user_id, friend_id=friend_id).evaluate()
    return jsonify({'are_friends': result})

# Récupérer les amis d’un utilisateur
@user_routes.route('/users/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    graph = current_app.graph
    query = """
    MATCH (u:User {id: $user_id})-[:FRIENDS_WITH]-(f:User)
    RETURN f
    """
    result = graph.run(query, user_id=user_id).data()
    return jsonify(result)

# Récupérer les amis en commun
@user_routes.route('/users/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def mutual_friends(user_id, other_id):
    graph = current_app.graph
    query = """
    MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(u2:User {id: $other_id})
    RETURN mutual
    """
    result = graph.run(query, user_id=user_id, other_id=other_id).data()
    return jsonify(result)
