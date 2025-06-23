from flask import Blueprint

instructor = Blueprint("instructor", __name__, url_prefix="/instructor")

from app.instructor import routes