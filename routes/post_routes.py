from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

post_routes = Blueprint('post_routes', __name__)

# Créer un post lié à un utilisateur
@post_routes.route('/users/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    graph = current_app.graph
    data = request.get_json()
    post_id = str(uuid.uuid4())
    query = """
    MATCH (u:User {id: $user_id})
    CREATE (p:Post {
        id: $id,
        title: $title,
        content: $content,
        created_at: $created_at
    })
    CREATE (u)-[:CREATED]->(p)
    RETURN p
    """
    result = graph.run(query,
                       user_id=user_id,
                       id=post_id,
                       title=data['title'],
                       content=data['content'],
                       created_at=str(datetime.utcnow())).data()
    return jsonify(result), 201

# Obtenir tous les posts
@post_routes.route('/posts', methods=['GET'])
def get_all_posts():
    graph = current_app.graph
    result = graph.run("MATCH (p:Post) RETURN p").data()
    return jsonify(result)

# Obtenir un post par ID
@post_routes.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    graph = current_app.graph
    result = graph.run("MATCH (p:Post {id: $id}) RETURN p", id=post_id).data()
    return jsonify(result[0]) if result else ('Post not found', 404)

# Obtenir les posts d’un utilisateur
@post_routes.route('/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    graph = current_app.graph
    query = """
    MATCH (u:User {id: $id})-[:CREATED]->(p:Post)
    RETURN p
    """
    result = graph.run(query, id=user_id).data()
    return jsonify(result)

# Mettre à jour un post
@post_routes.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    graph = current_app.graph
    data = request.get_json()
    query = """
    MATCH (p:Post {id: $id})
    SET p.title = $title, p.content = $content
    RETURN p
    """
    result = graph.run(query, id=post_id, title=data['title'], content=data['content']).data()
    return jsonify(result)

# Supprimer un post
@post_routes.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    graph = current_app.graph
    graph.run("MATCH (p:Post {id: $id}) DETACH DELETE p", id=post_id)
    return '', 204

# Ajouter un like à un post
@post_routes.route('/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    graph = current_app.graph
    data = request.get_json()
    user_id = data['user_id']
    query = """
    MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
    MERGE (u)-[:LIKES]->(p)
    """
    graph.run(query, user_id=user_id, post_id=post_id)
    return '', 204

# Retirer un like d’un post
@post_routes.route('/posts/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    graph = current_app.graph
    data = request.get_json()
    user_id = data['user_id']
    query = """
    MATCH (u:User {id: $user_id})-[l:LIKES]->(p:Post {id: $post_id})
    DELETE l
    """
    graph.run(query, user_id=user_id, post_id=post_id)
    return '', 204