from flask import Blueprint, jsonify

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/ping', methods=['GET'])
def ping_instructor():
    return jsonify({"message": "Instructor route working!"}), 200
