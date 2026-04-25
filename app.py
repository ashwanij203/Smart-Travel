from flask import Flask, request, jsonify, render_template
import requests as http_requests
import os
import json

app = Flask(__name__)

# Use environment variable for API key (set GEMINI_API_KEY in Vercel dashboard)
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAUM31kK1v5SY0VBQBVf8v_b4yTeeTNeK0")
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

SYSTEM_PROMPT = (
    "You are an AI trained to act as a personal travel assistant named SmartTravel AI. "
    "Only answer questions related to travel planning, destination suggestions, "
    "itinerary creation, budget tips, local experiences, and travel safety. "
    "Keep your responses helpful, concise, and friendly. "
    "If someone greets you, greet them back warmly and ask how you can help with their travel plans."
)

@app.route("/")
def home():
    return render_template("Index.html")

@app.route("/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "No message received."}), 400

    try:
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{SYSTEM_PROMPT}\n\nUser message: {user_message}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024
            }
        }

        headers = {"Content-Type": "application/json"}
        response = http_requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply_text})
        elif response.status_code == 429:
            return jsonify({"reply": "⏳ Our AI assistant is experiencing high demand right now. Please wait a moment and try again."})
        elif response.status_code == 403:
            return jsonify({"reply": "🔑 API key issue. Please check the GEMINI_API_KEY configuration."})
        else:
            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            return jsonify({"reply": f"😔 API error ({response.status_code}): {error_detail[:200]}"})

    except http_requests.exceptions.Timeout:
        return jsonify({"reply": "⏱️ The request timed out. Please try again."})
    except Exception as e:
        return jsonify({"reply": f"😔 Error: {str(e)[:200]}"})

if __name__ == "__main__":
    app.run(debug=True)
