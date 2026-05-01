from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from .models import db
from .routes import movies_bp

# Load environment variables from the shared .env file at the project root
# Path adjusted for being inside the 'app' subfolder (one level deeper)
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '../../../.env')
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'INVENTORY_DATABASE_URL', 'postgresql://user:password@localhost:5432/movies_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(movies_bp, url_prefix='/api')

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    with app.app_context():
        db.create_all()

    return app