import React, { useState } from "react";
import "./App.css";

const API_URL = process.env.REACT_APP_API_URL || "/api";

function App() {
  const [guess, setGuess] = useState("");
  const [message, setMessage] = useState("");
  const [attempts, setAttempts] = useState(null);
  const [highscore, setHighscore] = useState(null);
  const [loading, setLoading] = useState(false);

  async function sendGuess() {
    const value = parseInt(guess, 10);
    if (isNaN(value)) {
      setMessage("Introdu un număr valid.");
      return;
    }

    try {
      setLoading(true);
      const resp = await fetch(`${API_URL}/guess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ value }),
      });

      const data = await resp.json();

      if (data.result === "low") setMessage("Prea mic!");
      else if (data.result === "high") setMessage("Prea mare!");
      else if (data.result === "correct")
        setMessage(`Corect! Numărul era ${data.number}.`);

      if (data.attempts !== undefined) setAttempts(data.attempts);
    } catch (err) {
      console.error(err);
      setMessage("Eroare la comunicarea cu serverul.");
    } finally {
      setLoading(false);
    }
  }

  async function resetGame() {
    try {
      setLoading(true);
      await fetch(`${API_URL}/reset`, { method: "POST" });
      setMessage("Joc resetat.");
      setAttempts(null);
    } catch (err) {
      console.error(err);
      setMessage("Eroare la reset.");
    } finally {
      setLoading(false);
    }
  }

  async function loadHighscore() {
    try {
      setLoading(true);
      const resp = await fetch(`${API_URL}/highscore`);
      const data = await resp.json();
      setHighscore(data);
    } catch (err) {
      console.error(err);
      setMessage("Nu am putut încărca scorul maxim.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Jocul de Ghicit Numere</h1>
        <p>Ghiceste numărul între 1 și 100.</p>

        <div style={{ marginBottom: "1rem" }}>
          <input
            type="number"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            placeholder="Introdu un număr"
          />
          <button onClick={sendGuess} disabled={loading}>
            Ghiceste
          </button>
          <button onClick={resetGame} disabled={loading}>
            Reset
          </button>
        </div>

        {message && <p>{message}</p>}
        {attempts !== null && <p>Încercări: {attempts}</p>}

        <div style={{ marginTop: "2rem" }}>
          <button onClick={loadHighscore} disabled={loading}>
            Vezi Highscore
          </button>
          {highscore && (
            <p>
              Highscore: {highscore.best_attempts} încercări (jucător:{" "}
              {highscore.player || "Anonim"})
            </p>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
