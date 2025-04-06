from flask import Flask, request, jsonify
from flask import Flask, render_template

import google.generativeai as genai
import os
#from flask_cors import CORS  # Optional, for frontend-backend communication
chat_history = []
app = Flask(__name__)
TRAVEL_KEYWORDS = [
    "trip", "travel", "vacation", "holiday", "destination", "place", "city",
    "country", "hotel", "flight", "journey", "itinerary", "tour", "explore",
    "sightseeing", "adventure", "package", "booking", "resort", "beach", "mountain"
]

def is_travel_related(message):
    message = message.lower()
    return any(keyword in message for keyword in TRAVEL_KEYWORDS)
#CORS(app)  # Optional for development
@app.route("/")
def home():
    return render_template("Index.html")
genai.configure(api_key="AIzaSyAuCfBJrx3gSWfeiWHp73I1wKg9wGF5g_Y")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/get-response", methods=["POST"])

def get_response():
    data = request.get_json()
    user_message = data.get("message")
    if not is_travel_related(user_message):
        return jsonify({"reply": "I'm your travel assistant 🧳✨ Please ask travel-related questions only."})
    else:
        if not user_message:
            return jsonify({"reply": "No message received"}), 400

        try:
            response = model.generate_content(user_message)
            return jsonify({"reply": response.text})
        except Exception as e:
            return jsonify({"reply": "Error from Gemini API"}), 500
if __name__ == "__main__":
    app.run(debug=True)