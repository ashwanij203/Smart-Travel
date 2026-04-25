from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

TRAVEL_KEYWORDS = [
    "trip", "travel", "vacation", "holiday", "destination", "place", "city",
    "country", "hotel", "flight", "journey", "itinerary", "tour", "explore",
    "sightseeing", "adventure", "package", "booking", "resort", "beach", "mountain"
]

def is_travel_related(message):
    message = message.lower()
    return any(keyword in message for keyword in TRAVEL_KEYWORDS)

# Use environment variable for API key (set GEMINI_API_KEY in Vercel dashboard)
api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyAUM31kK1v5SY0VBQBVf8v_b4yTeeTNeK0")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

SYSTEM_PROMPT = "You are an AI trained to act as a personal travel assistant. Only answer questions related to travel planning, destination suggestions, itinerary creation, budget tips, local experiences, and travel safety. Keep your responses helpful, concise, and friendly."

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
        # Use generate_content instead of chat session for stateless serverless
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
        response = model.generate_content(full_prompt)
        reply_text = response.text if response.text else "I'm here to support you with your travel plans!"
        return jsonify({"reply": reply_text})
    except Exception as e:
        error_str = str(e).lower()
        print(f"Gemini API Error: {str(e)}")  # Log for Vercel
        if "quota" in error_str or "rate_limit" in error_str or "429" in error_str:
            return jsonify({"reply": "⏳ Our AI assistant is experiencing high demand right now. Please wait a moment and try again."})
        elif "api_key" in error_str or "authentication" in error_str or "403" in error_str:
            return jsonify({"reply": "🔑 There's a configuration issue with the AI service. The team has been notified."})
        elif "404" in error_str or "not found" in error_str:
            return jsonify({"reply": "🔧 The AI model is being updated. Please try again shortly."})
        else:
            return jsonify({"reply": f"😔 Something went wrong: {str(e)[:150]}"})

if __name__ == "__main__":
    app.run(debug=True)
