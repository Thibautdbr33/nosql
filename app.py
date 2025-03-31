from flask import Flask
from py2neo import Graph
from routes.user_routes import user_routes
from routes.post_routes import post_routes
from routes.comment_routes import comment_routes

app = Flask(__name__)

# Connexion à Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))
app.graph = graph

# Enregistrement des Blueprints (routes)
app.register_blueprint(user_routes)
app.register_blueprint(post_routes)
app.register_blueprint(comment_routes)

# Route de test
@app.route('/ping')
def ping():
    return {"message": "pong"}

if __name__ == '__main__':
    app.run(debug=True)
