from flask import Flask, Blueprint
from app.routes.main.routes import main
from app.routes.api.routes import api
from app.config import SECRET_KEY
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
 
    app.register_blueprint(main)
    app.register_blueprint(api)

    return app
