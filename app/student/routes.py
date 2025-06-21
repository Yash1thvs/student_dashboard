from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Enrollment, Course
from app.extensions import db

from app.student import student

# GET /student/courses - Get all courses the student is enrolled in
@student.route("/courses", methods=["GET"])
@jwt_required()
def get_enrolled_courses():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "student":
        return jsonify({"msg": "Unauthorized access"}), 403

    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    enrolled_courses = []

    for enrollment in enrollments:
        course = Course.query.get(enrollment.course_id)
        enrolled_courses.append({
            "course_id": course.id,
            "name": course.name,
            "thumbnail": course.thumbnail,
            "due_date": course.due_date.strftime('%Y-%m-%d'),
            "progress": enrollment.progress,
            "is_completed": enrollment.is_completed
        })

    return jsonify(enrolled_courses), 200


# GET /student/courses/<course_id> - Get details of a specific course
@student.route("/courses/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course_details(course_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "student":
        return jsonify({"msg": "Unauthorized access"}), 403

    enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    if not enrollment:
        return jsonify({"msg": "You are not enrolled in this course"}), 404

    course = Course.query.get(course_id)
    return jsonify({
        "course_id": course.id,
        "name": course.name,
        "thumbnail": course.thumbnail,
        "due_date": course.due_date.strftime('%Y-%m-%d'),
        "progress": enrollment.progress,
        "is_completed": enrollment.is_completed
    }), 200


# POST /student/courses/<course_id>/progress - Update course progress
@student.route("/courses/<int:course_id>/progress", methods=["POST"])
@jwt_required()
def update_course_progress(course_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "student":
        return jsonify({"msg": "Unauthorized access"}), 403

    data = request.get_json()
    new_progress = data.get("progress")

    if new_progress is None or not isinstance(new_progress, int) or not (0 <= new_progress <= 100):
        return jsonify({"msg": "Progress must be an integer between 0 and 100"}), 400

    enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    if not enrollment:
        return jsonify({"msg": "You are not enrolled in this course"}), 404

    enrollment.progress = new_progress
    if new_progress == 100:
        enrollment.is_completed = True

    db.session.commit()
    return jsonify({"msg": "Progress updated successfully"}), 200


# ✅ POST /student/enroll/<course_id> - Enroll in a course
@student.route("/enroll/<int:course_id>", methods=["POST"])
@jwt_required()
def enroll_in_course(course_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "student":
        return jsonify({"msg": "Unauthorized access"}), 403

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"msg": "Course not found"}), 404

    existing_enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({"msg": "Already enrolled in this course"}), 400

    enrollment = Enrollment(student_id=user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({"msg": f"Enrolled in course '{course.name}' successfully"}), 201
