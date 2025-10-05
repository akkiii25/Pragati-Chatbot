from flask import Flask, render_template, request, jsonify
from bot import Pragati

app = Flask(__name__)

bot = Pragati()

@app.route("/")
def index():
    """Render chat page"""
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    """Handle user messages and return bot reply"""
    user_message = request.json.get("message", "")
    if not user_message.strip():
        return jsonify({"reply": "Please type something."})

    reply = bot.get_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)