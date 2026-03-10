from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Config
    # Ensure instance directory exists for SQLite
    db_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/insuresmart_db')
    if db_url.startswith('sqlite:///'):
        # Extract path from sqlite URL and create directory
        db_path = db_url.replace('sqlite:///', '')
        if db_path.startswith('./'):
            db_path = db_path[2:]  # Remove './' prefix
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    from app.routes import core_bp, auth_bp, policy_bp, ai_bp
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(ai_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
