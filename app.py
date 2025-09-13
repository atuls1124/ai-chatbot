from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "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"
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(BASE_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
