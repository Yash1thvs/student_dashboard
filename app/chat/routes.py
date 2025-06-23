from openai import OpenAI
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Chat, db  # Adjust imports as needed
from dotenv import load_dotenv

from app.chat import chat

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

    # Get response from OpenAI using new SDK format
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful academic assistant."},
                {"role": "user", "content": message}
            ]
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"msg": "Failed to connect to LLM", "error": str(e)}), 500

    # Save chat to DB
    chat = Chat(student_id=user.id, message=message, response=reply)
    db.session.add(chat)
    db.session.commit()

    return jsonify({"response": reply}), 200


@chat.route("/chat/history", methods=["GET"])
@jwt_required()
def get_chat_history():
    user_id = get_jwt_identity()
    history = Chat.query.filter_by(student_id=user_id).order_by(Chat.timestamp).all()

    messages = []
    for msg in history:
        messages.append({
            "sender": "user",
            "text": msg.message,
            "timestamp": msg.timestamp.isoformat()
        })
        messages.append({
            "sender": "bot",
            "text": msg.response,
            "timestamp": msg.timestamp.isoformat()
        })

    return jsonify(messages), 200


@chat.route("/chat/history", methods=["DELETE"])
@jwt_required()
def clear_chat_history():
    user_id = get_jwt_identity()
    Chat.query.filter_by(student_id=user_id).delete()
    db.session.commit()
    return jsonify({"msg": "Chat history cleared."}), 200


