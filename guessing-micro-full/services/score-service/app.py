from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from pathlib import Path

DB_PATH = Path("/data/score.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS scores(id INTEGER PRIMARY KEY, score INTEGER, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="Score Service")

class ScoreIn(BaseModel):
    score: int

@app.post("/score")
def save_score(payload: ScoreIn):
    conn = get_conn()
    conn.execute("INSERT INTO scores(score) VALUES (?)", (payload.score,))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.get("/scores")
def get_scores(limit: int = 10):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM scores ORDER BY ts DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return {"scores":[dict(r) for r in rows]}
