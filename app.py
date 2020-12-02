import os
from flask import Flask, jsonify, g
import models
from flask_login import LoginManager
from flask_cors import CORS
from blueprints.users import user
from blueprints.recipes import recipe

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "flask is dumb"
login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user

    except models.DoesNotExist:
        return None
CORS(recipe, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user, url_prefix='/pandemic-pantry/users/')
app.register_blueprint(recipe, url_prefix='/pandemic-pantry/recipes/')
# The default URL ends in / ("my-website.com/").

@app.before_request
def before_request():
    """Connect to the db before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Connect to the db before each request"""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)