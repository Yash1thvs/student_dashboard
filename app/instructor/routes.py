from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Course, Enrollment
from app.extensions import db
from datetime import datetime

from app.instructor import instructor

# POST /instructor/courses – Create New Course
@instructor.route("/courses", methods=["POST"])
@jwt_required()
def create_course():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "instructor":
        return jsonify({"msg": "Unauthorized access"}), 403


    data = request.get_json()
    name = data.get("name")
    thumbnail = data.get("thumbnail")
    due_date = data.get("due_date")  # Expected format: 'YYYY-MM-DD'

    if not name or not due_date:
        return jsonify({"msg": "Name and due_date are required"}), 400

    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    course = Course(
        name=name,
        thumbnail=thumbnail,
        due_date=due_date_obj,
        instructor_id=user.id
    )
    db.session.add(course)
    db.session.commit()

    return jsonify({"msg": "Course created successfully", "course_id": course.id}), 201

# GET /instructor/courses – View Created Courses
@instructor.route("/courses", methods=["GET"])
@jwt_required()
def get_instructor_courses():
    current_user_id = int(get_jwt_identity())
    instructor = User.query.get(current_user_id)

    if not instructor or instructor.role != "instructor":
        return jsonify({"msg": "Unauthorized access"}), 403

    courses = Course.query.filter_by(instructor_id=instructor.id).all()
    result = []

    for course in courses:
        enrollments = Enrollment.query.filter_by(course_id=course.id).all()

        enrolled_students = []
        total_progress = 0
        for enrollment in enrollments:
            student = User.query.get(enrollment.student_id)
            enrolled_students.append({
                "id": student.id,
                "name": student.name,
                "progress": enrollment.progress
            })
            total_progress += enrollment.progress

        enrollment_count = len(enrollments)
        completion_percentage = (
            int(total_progress / enrollment_count) if enrollment_count > 0 else 0
        )

        result.append({
            "id": course.id,
            "name": course.name,
            "thumbnail": course.thumbnail,
            "due_date": course.due_date.strftime("%Y-%m-%d"),
            "enrollment_count": enrollment_count,
            "completion_percentage": completion_percentage,
            "enrolled_students": enrolled_students
        })

    return jsonify(result), 200

# GET /instructor/courses/<course_id>/students
@instructor.route("/courses/<int:course_id>/students", methods=["GET"])
@jwt_required()
def get_enrolled_students(course_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user or user.role != "instructor":
        return jsonify({"msg": "Unauthorized access"}), 403

    course = Course.query.filter_by(id=course_id, instructor_id=user.id).first()
    if not course:
        return jsonify({"msg": "Course not found or not owned by instructor"}), 404

    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [
        {
            "student_id": e.student.id,
            "name": e.student.name,
            "email": e.student.email,
            "progress": e.progress,
            "is_completed": e.is_completed
        }
        for e in enrollments
    ]

    return jsonify(students), 200

