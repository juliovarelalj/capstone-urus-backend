import os
import openai
from flask import Blueprint, request, jsonify, render_template
from app.auth import login_required

chat_bp = Blueprint("chat_bp", __name__, url_prefix="/chat")

# Configura la API key de OpenAI desde tu archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@chat_bp.route("", methods=["GET"])
@login_required
def chat_page():
    """Muestra la interfaz del chatbot."""
    return render_template("chat.html")

@chat_bp.route("/ask", methods=["POST"])
@login_required
def ask():
    """
    Recibe un mensaje del usuario, lo envía a la API de OpenAI con el modelo GPT-4o mini
    y devuelve la respuesta.
    """
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400

    try:
        # Usamos la API de ChatCompletion (GPT) con el modelo "GPT-4o mini"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",  # Ajusta el nombre del modelo según tu acceso real
            messages=[
                {"role": "system", "content": "Eres un chatbot de inversión. Devuelve tus respuestas en formato Markdown, con títulos y viñetas cuando sea apropiado."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        # Obtenemos la respuesta  gpt-4o-mini-2024-07-18
        answer = response.choices[0].message["content"].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
