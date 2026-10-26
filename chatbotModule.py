
import os

from flask import Blueprint, jsonify, request  # pyright: ignore[reportMissingImports]
from google import genai

chatbot_bp = Blueprint("chatbot", __name__)

SYSTEM_PROMPT = """
You are KrishiMitra AI, a helpful agricultural assistant for farmers in India.

Your responsibilities:
- Answer questions about crops, sowing, irrigation, soil health,
  nutrients, common plant diseases, pests and farming practices.
- Explain answers in simple language.
- Respond in Hindi when the farmer asks in Hindi, and in English
  when the farmer asks in English.
- Ask for the crop, location, season or symptoms when important
  information is missing.
- Give practical, cautious, easy-to-understand suggestions.
- Never invent government schemes, current mandi prices or live
  weather information. Explain when information needs verification.
- Do not claim that a plant disease is confirmed from a text description.
- For pesticide or fertilizer use, advise following the product label
  and local agricultural expert guidance. Do not invent dosages.
- If a question is outside agriculture, politely guide the user back
  to farming assistance.
- Be respectful and supportive of farmers.
"""

@chatbot_bp.route("/api/chat", methods=["POST"])
def chat():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return jsonify({
                "error": "The chatbot API key is not configured."
            }), 503

        data = request.get_json(silent=True) or {}
        message = data.get("message", "")

        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "error": "Please enter your question."
            }), 400

        if len(message) > 2000:
            return jsonify({
                "error": "Please keep your question under 2000 characters."
            }), 400

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message.strip(),
            config=type.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=600,
            ),
        )

        answer = response.text

        if not answer:
            return jsonify({
                "error": "I could not prepare an answer. Please try again."
            }), 502

        return jsonify({"reply": answer})

    except Exception:
        chatbot_bp.logger.exception("KrishiMitra chatbot error")
        return jsonify({
            "error": "The AI assistant is temporarily unavailable. Please try again."
        }), 502
