from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "scoredb")
DB_USER = os.getenv("DB_USER", "scoreuser")
DB_PASS = os.getenv("DB_PASS", "secret123")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ensure table exists
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS highscores (
            id SERIAL PRIMARY KEY,
            player VARCHAR(255),
            attempts INT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/highscore", methods=["GET"])
def get_highscore():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT player, attempts FROM highscores ORDER BY attempts ASC LIMIT 1;")
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return jsonify({"player": row[0], "best_attempts": row[1]})
    else:
        return jsonify({"player": None, "best_attempts": None})

@app.route("/highscore", methods=["POST"])
def submit_score():
    data = request.json
    player = data.get("player", "Anonim")
    attempts = data.get("attempts")

    if attempts is None:
        return jsonify({"error": "Missing attempts"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO highscores (player, attempts) VALUES (%s, %s);",
        (player, attempts)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Score saved!"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8001)
