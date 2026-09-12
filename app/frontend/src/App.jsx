import { useState } from "react";
import EmailForm from "./components/EmailForm.jsx";
import ResultCard from "./components/ResultCard.jsx";
import { predictEmail } from "./api.js";
import "./App.css";

export default function App() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await predictEmail(subject, body);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Phishing Email Detector</h1>
        <p className="subtitle">
          Paste an email's subject and body to check whether it looks like phishing.
        </p>
      </header>

      <main>
        <EmailForm
          subject={subject}
          body={body}
          onSubjectChange={setSubject}
          onBodyChange={setBody}
          onSubmit={handleSubmit}
          loading={loading}
        />

        {loading && <div className="status status-loading">Analyzing email...</div>}
        {error && <div className="status status-error">{error}</div>}
        {!loading && !error && <ResultCard result={result} />}
      </main>

      <footer>
        <p>Model: TF-IDF + Logistic Regression, trained on labeled phishing/legitimate emails.</p>
      </footer>
    </div>
  );
}
