from flask import Flask
from .route import services_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(services_bp)
    return app