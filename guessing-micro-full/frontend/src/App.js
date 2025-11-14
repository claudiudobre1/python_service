import './App.css';
import React, { useState } from 'react';

function App() {
  const apiRoot = "http://34.116.157.63/api"; // trimite prin gateway către backend

  const [guess, setGuess] = useState("");
  const [result, setResult] = useState("");
  const [attempts, setAttempts] = useState("");

  async function sendGuess() {
    if (!guess) return;

    const resp = await fetch(`${apiRoot}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value: parseInt(guess, 10) })
    });

    const data = await resp.json();

    if (data.result === "low") setResult("Prea mic!");
    else if (data.result === "high") setResult("Prea mare!");
    else if (data.result === "correct") {
      setResult(`Corect! Numărul era ${data.number}.`);
    }

    if (data.attempts) setAttempts(`Încercări: ${data.attempts}`);
  }

  async function resetGame() {
    await fetch(`${apiRoot}/reset`, { method: "POST" });
    setResult("Joc resetat.");
    setAttempts("");
    setGuess("");
  }

  return (
    <div style={{ maxWidth: "400px", margin: "40px auto", fontFamily: "Arial" }}>
      <h1>🎯 Jocul de Ghicit Numere</h1>
      <p>Ghiceste un număr între 1 și 100.</p>

      <input
        type="number"
        value={guess}
        onChange={(e) => setGuess(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        placeholder="Introdu un număr"
      />

      <button onClick={sendGuess} style={{ padding: "10px", width: "48%", marginRight: "4%" }}>
        Ghicește
      </button>
      <button onClick={resetGame} style={{ padding: "10px", width: "48%" }}>
        Reset
      </button>

      <h2 style={{ marginTop: "20px" }}>{result}</h2>
      <p>{attempts}</p>
    </div>
  );
}

export default App;
