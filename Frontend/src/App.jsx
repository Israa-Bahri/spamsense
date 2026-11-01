import { useState } from "react";
import Layout from "./Layout";

const LIMITATION =
  "Demo only. This model was trained on SMS spam, so it is not a fraud detector. " +
  "\"Not flagged\" does not mean a message is safe.";

export default function App() {
  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  const [label, setLabel] = useState(null);

  const [spamProb, setSpamProb] = useState(null);

  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (loading) return; // ignore clicks while a request is running

    if (message.trim() === "") {
      setError("Please paste a message first.");
      setLabel(null);
      return;
    }

    setLoading(true);
    setError("");
    setLabel(null);

   
    // If anything fails, JavaScript jumps to "catch" instead of breaking the page.
    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      // data stays as an empty object instead of crashing.
      let data = {};
      try {
        data = await res.json();
      } catch {
        // not JSON, ignore
      }

      // CASE 2: the server is running but answered with an error (422, 500, 503...)
      if (!res.ok) {
        setError(
          data.error || data.detail || `Server error (${res.status}). Please try again.`
        );
        return;
      }

      setLabel(data.prediction);
      setSpamProb(data.spam_probability);
    } catch {
      setError("Backend unavailable. Please check that the server is running and try again.");
    } finally {
      setLoading(false); 
    }
  }

  const labelText = label === "spam" ? "Spam-like" : "Not flagged by model";

  return (
    <Layout>
      <h1>SMS Spam Checker</h1>
      <p>Check whether a message looks like spam</p>

      <section className="analyzer">
        <h2>Analyzer</h2>

    
        <textarea
          id="message-input"
          placeholder="Paste a message here"
          rows="5"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        
        <p className="privacy-note"><strong>Privacy:</strong> Don't paste passwords, bank or card details, or other
  sensitive personal information. Your message is sent to the server only to get a
  prediction. This app does not save it.
</p>


        
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze message"}
        </button>

        
        <div aria-live="polite">
          {error && (
            <div className="result result-error" role="alert">
              {error}
            </div>
          )}

          {label && (
            <div className={`result result-${label}`}>
              <strong>{labelText}</strong>
              <span> ({Math.round(spamProb * 100)}% spam score)</span>
              <p className="limitation">{LIMITATION}</p>
            </div>
          )}
        </div>
      </section>
    </Layout>
  );
}