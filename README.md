# Smart-Travel
An AI-powered web-based assistant that helps users create smart packing lists based on their travel preferences and inputs. This project combines a simple web interface with a backend powered by gemini.
📂 Project Structure
bash
Copy
Edit
AI-Smart-Travel-Packing-Assistant/
│
├── Index.html       # Frontend user interface (HTML + inline CSS/JS)
├── app.py           # Flask-based Python backend integrating OpenAI API
├── README.md        # Project documentation
🚀 Features
User-friendly interface for inputting travel details.

Text-based AI assistant generating personalized packing lists.

Flask backend for handling requests and OpenAI integration.

Smooth client-server interaction with AJAX (JavaScript).

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript (AJAX)

Backend: Python (Flask)

AI Model: OpenAI GPT-3.5-turbo (via OpenAI API)

🔧 Installation & Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/AI-Smart-Travel-Packing-Assistant.git
cd AI-Smart-Travel-Packing-Assistant
Install dependencies

bash
Copy
Edit
pip install flask openai
Set your OpenAI API key

In app.py, replace "your-api-key" with your actual OpenAI API key:

python
Copy
Edit
openai.api_key = "your-api-key"
Run the Flask server

bash
Copy
Edit
python app.py
Open in browser

Navigate to http://127.0.0.1:5000 and start using the assistant.

💡 How It Works
User enters travel details in the web form.

JavaScript sends the input to the Flask server via AJAX.

Flask backend queries OpenAI's model using the input.

OpenAI returns a smart packing suggestion.

The suggestion is displayed on the webpage.

📸 Preview
You can include screenshots or a short demo video link here.

📌 To Do / Future Enhancements
🎤 Add voice input/output support.

📱 Make the UI responsive and mobile-friendly.

🌍 Support multi-language interaction.

💾 Store user sessions/history.

☁️ Deploy on a cloud platform (e.g., Render, Vercel, or Heroku).
