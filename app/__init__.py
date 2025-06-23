from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from flask_cors import CORS

# Import your blueprints (routes)
from app.auth.routes import auth
from app.student.routes import student
from app.instructor.routes import instructor
from app.chat.routes import chat
from app.courses.routes import course_bp

# Import models to register with SQLAlchemy
from app.models import models  # Needed for migrations

from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(instructor)
    app.register_blueprint(chat)
    app.register_blueprint(course_bp)

    return app
