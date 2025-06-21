from flask import Blueprint, jsonify

student_bp = Blueprint('student', __name__)

@student_bp.route('/ping', methods=['GET'])
def ping_student():
    return jsonify({"message": "Student route working!"}), 200
