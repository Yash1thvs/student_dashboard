from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt

# Import your blueprints (routes)
from app.auth.routes import auth_bp
# from app.routes.auth import auth_bp
# from app.routes.student import student_bp
# from app.routes.instructor import instructor_bp

# Import models to register with SQLAlchemy
from app.models import models  # Needed for migrations

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    # app.register_blueprint(student_bp, url_prefix="/student")
    # app.register_blueprint(instructor_bp, url_prefix="/instructor")

    return app
