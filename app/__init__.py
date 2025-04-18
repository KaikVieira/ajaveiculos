import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import cloudinary
from urllib.parse import urlparse

db = SQLAlchemy()

def configure_cloudinary():
    cloudinary_url = os.getenv('CLOUDINARY_URL')
    parsed_url = urlparse(cloudinary_url)

    cloudinary.config(
        cloud_name=parsed_url.hostname,
        api_key=parsed_url.username,
        api_secret=parsed_url.password
    )

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    database_path = os.environ.get('DATABASE_URL', None)
    if database_path is None:
        database_path = f'sqlite:///{os.path.join(base_dir, "instance", "carros.db")}'
    else:
        database_path = database_path.replace("postgres://", "postgresql://")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  

    app.config['USUARIO_ADMIN'] = os.getenv('USUARIO_ADMIN')
    app.config['SENHA_ADMIN'] = os.getenv('SENHA_ADMIN')
    app.config['TOKEN_ACESSO'] = os.getenv('TOKEN_ACESSO')

    os.makedirs(os.path.join(base_dir, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    configure_cloudinary()

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
