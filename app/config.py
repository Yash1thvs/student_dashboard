import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:yash@localhost/student_dashboard_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
