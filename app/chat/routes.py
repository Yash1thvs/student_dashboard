from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Chat
import openai
import os

from app.chat import chat

@chat.route("/chat", methods=["POST"])
@jwt_required()
def chat_with_bot():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or user.role != "student":
        return jsonify({"msg": "Unauthorized access"}), 403

    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"msg": "Message is required"}), 400

    # Get response from OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful academic assistant."},
                {"role": "user", "content": message}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        return jsonify({"msg": "Failed to connect to LLM", "error": str(e)}), 500

    # Save to DB
    chat = Chat(student_id=user.id, message=message, response=reply)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"response": reply}), 200
