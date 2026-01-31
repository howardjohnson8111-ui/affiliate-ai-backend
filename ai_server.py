from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import threading

from ai_service import AffiliateAIExecutive

API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    print("[WARNING] GOOGLE_API_KEY environment variable not set for ai_server!")

app = Flask(__name__)
CORS(app)

# Create a singleton assistant to reuse across requests
assistant = None
assistant_lock = threading.Lock()

def get_assistant():
    global assistant
    with assistant_lock:
        if assistant is None:
            assistant = AffiliateAIExecutive()
        return assistant

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    user_message = data.get('message')
    try:
        assistant = get_assistant()
        response = assistant.chat(user_message)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5001 to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=False)
