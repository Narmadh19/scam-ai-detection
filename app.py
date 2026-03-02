from flask import Flask, request, jsonify
import re
from pyzbar.pyzbar import decode
from PIL import Image
import speech_recognition as sr

app = Flask(__name__)

def url_risk_score(message):
    urls = re.findall(r'(https?://\S+)', message)
    if not urls:
        return 0

    url = urls[0]
    score = 0

    if url.startswith("http://"):
        score += 30

    suspicious_words = ["verify", "login", "bank", "update", "secure", "account"]
    for word in suspicious_words:
        if word in url.lower():
            score += 15

    if len(url) > 50:
        score += 20

    if url.count('.') > 3:
        score += 15

    return min(score, 100)


@app.route("/")
def home():
    return "Scam Detection AI is Running 🚀"


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    message = data.get("message", "")
    score = url_risk_score(message)

    if score == 0:
        result = "Low Risk"
    elif score < 40:
        result = "Medium Risk"
    else:
        result = "High Risk"

    return jsonify({
        "risk_score": score,
        "risk_level": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)