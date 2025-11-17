import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

GAME_URL = os.getenv("GAME_URL", "http://game-service:8000")
SCORE_URL = os.getenv("SCORE_URL", "http://score-service:8001")

@app.route("/api/guess", methods=["POST"])
def guess():
    data = request.get_json()
    r = requests.post(f"{GAME_URL}/guess", json=data)
    return jsonify(r.json())

@app.route("/api/reset", methods=["POST"])
def reset():
    r = requests.post(f"{GAME_URL}/reset")
    return jsonify(r.json())

@app.route("/api/highscore", methods=["GET"])
def api_highscore():
    try:
        r = requests.get(f"{SCORE_URL}/highscore")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/highscore", methods=["POST"])
def api_submit_score():
    data = request.json
    try:
        r = requests.post(f"{SCORE_URL}/highscore", json=data)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
