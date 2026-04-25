from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

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

# Use environment variable for API key (set GEMINI_API_KEY in Vercel dashboard)
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAuCfBJrx3gSWfeiWHp73I1wKg9wGF5g_Y")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

chat_session = model.start_chat(history=[
{
    "role": "user",
    "parts": [
        "You are an AI trained to act as a personal travel assistant. Only answer questions related to travel planning, destination suggestions, itinerary creation, budget tips, local experiences, and travel safety."
    ]
}
])

@app.route("/get-response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"reply": "No message received."}), 400

    try:
        response = chat_session.send_message(user_message)
        reply_text = response.text if response.text else "I'm here to support you with your travel plans!"
        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"reply": f"Sorry, I encountered an error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
