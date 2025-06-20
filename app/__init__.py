from flask import Flask
from flask_restx import Api
from .config import Config
from .extensions import db, migrate, jwt

# Import route namespaces
from .routes.auth_routes import api as auth_ns
from .routes.student_routes import api as student_ns
from .routes.instructor_routes import api as instructor_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # API setup
    api = Api(app, title="Student Dashboard API", version="1.0", doc="/docs")

    # Register Namespaces
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(student_ns, path="/student")
    api.add_namespace(instructor_ns, path="/instructor")

    return app
