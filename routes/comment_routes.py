from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

comment_routes = Blueprint('comment_routes', __name__)

# Ajouter un commentaire à un post (créateur + relation post)
@comment_routes.route('/posts/<post_id>/comments', methods=['POST'])
def add_comment(post_id):
    graph = current_app.graph
    data = request.get_json()
    comment_id = str(uuid.uuid4())
    query = """
    MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
    CREATE (c:Comment {
        id: $id,
        content: $content,
        created_at: $created_at
    })
    CREATE (u)-[:CREATED]->(c)
    CREATE (p)-[:HAS_COMMENT]->(c)
    RETURN c
    """
    result = graph.run(query,
                       user_id=data['user_id'],
                       post_id=post_id,
                       id=comment_id,
                       content=data['content'],
                       created_at=str(datetime.utcnow())).data()
    return jsonify(result), 201

# Obtenir les commentaires d’un post
@comment_routes.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    graph = current_app.graph
    query = """
    MATCH (p:Post {id: $id})-[:HAS_COMMENT]->(c:Comment)
    RETURN c
    """
    result = graph.run(query, id=post_id).data()
    return jsonify(result)

# Supprimer un commentaire d’un post
@comment_routes.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment_from_post(post_id, comment_id):
    graph = current_app.graph
    query = "MATCH (c:Comment {id: $id}) DETACH DELETE c"
    graph.run(query, id=comment_id)
    return '', 204

# Obtenir tous les commentaires
@comment_routes.route('/comments', methods=['GET'])
def get_all_comments():
    graph = current_app.graph
    result = graph.run("MATCH (c:Comment) RETURN c").data()
    return jsonify(result)

# Obtenir un commentaire par ID
@comment_routes.route('/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    graph = current_app.graph
    result = graph.run("MATCH (c:Comment {id: $id}) RETURN c", id=comment_id).data()
    return jsonify(result[0]) if result else ('Comment not found', 404)

# Mettre à jour un commentaire
@comment_routes.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    graph = current_app.graph
    data = request.get_json()
    query = """
    MATCH (c:Comment {id: $id})
    SET c.content = $content
    RETURN c
    """
    result = graph.run(query, id=comment_id, content=data['content']).data()
    return jsonify(result)

# Supprimer un commentaire
@comment_routes.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    graph = current_app.graph
    graph.run("MATCH (c:Comment {id: $id}) DETACH DELETE c", id=comment_id)
    return '', 204

# Ajouter un like à un commentaire
@comment_routes.route('/comments/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    graph = current_app.graph
    data = request.get_json()
    query = """
    MATCH (u:User {id: $user_id}), (c:Comment {id: $comment_id})
    MERGE (u)-[:LIKES]->(c)
    """
    graph.run(query, user_id=data['user_id'], comment_id=comment_id)
    return '', 204

# Retirer un like d’un commentaire
@comment_routes.route('/comments/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    graph = current_app.graph
    data = request.get_json()
    query = """
    MATCH (u:User {id: $user_id})-[l:LIKES]->(c:Comment {id: $comment_id})
    DELETE l
    """
    graph.run(query, user_id=data['user_id'], comment_id=comment_id)
    return '', 204