from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Course

from app.courses import course_bp

@course_bp.route("/all", methods=["GET"])
# @jwt_required
def get_all_courses():
    courses = Course.query.all()
    result = [
        {
            "id": course.id,
            "name": course.name
        }
        for course in courses
    ]
    return jsonify(result), 200
