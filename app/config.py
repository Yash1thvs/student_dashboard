# import os
#
# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
#     SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yash@localhost/student_dashboard_db"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-jwt-secret-key")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
