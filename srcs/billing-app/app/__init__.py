from flask import Flask
from .model import db
from .config import Config

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=Config.BILLING_DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
