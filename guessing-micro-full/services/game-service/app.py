from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI(title="Game Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MIN_NUM = 1
MAX_NUM = 100

class Guess(BaseModel):
    value: int

# keep state simple (in-memory) — for production use Redis/DB
if "SECRET_NUMBER" in os.environ:
    secret = int(os.environ["SECRET_NUMBER"])
else:
    secret = random.randint(MIN_NUM, MAX_NUM)
attempts = 0

SCORE_SERVICE_URL = os.environ.get("SCORE_SERVICE_URL", "http://score-service:8001")

@app.get("/")
def root():
    return {"message": "Game Service running"}

@app.post("/guess")
def make_guess(guess: Guess):
    global secret, attempts
    attempts += 1
    if guess.value < secret:
        return {"result": "low", "attempts": attempts}
    if guess.value > secret:
        return {"result": "high", "attempts": attempts}
    # correct
    number = secret
    # report score to score-service (fire-and-forget)
    try:
        requests.post(f"{SCORE_SERVICE_URL}/score", json={"score": attempts}, timeout=1)
    except Exception:
        pass
    # reset
    secret = random.randint(MIN_NUM, MAX_NUM)
    attempts_before = attempts
    attempts = 0
    return {"result": "correct", "number": number, "attempts": attempts_before}

@app.post("/reset")
def reset():
    global secret, attempts
    secret = random.randint(MIN_NUM, MAX_NUM)
    attempts = 0
    return {"ok": True}
