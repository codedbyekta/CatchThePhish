export default function ResultCard({ result }) {
  if (!result) return null;

  const { is_phishing, phishing_probability, legitimate_probability } = result;
  const confidence = is_phishing ? phishing_probability : legitimate_probability;
  const confidencePercent = Math.round(confidence * 100);

  return (
    <div className={`result-card ${is_phishing ? "result-phishing" : "result-legitimate"}`}>
      <div className="result-icon">{is_phishing ? "⚠️" : "✅"}</div>
      <div className="result-text">
        <h2>{is_phishing ? "Likely Phishing" : "Likely Legitimate"}</h2>
        <p>Confidence: {confidencePercent}%</p>
        <div className="probability-bars">
          <div className="prob-row">
            <span>Phishing</span>
            <div className="bar-track">
              <div
                className="bar-fill phishing"
                style={{ width: `${Math.round(phishing_probability * 100)}%` }}
              />
            </div>
            <span>{Math.round(phishing_probability * 100)}%</span>
          </div>
          <div className="prob-row">
            <span>Legitimate</span>
            <div className="bar-track">
              <div
                className="bar-fill legitimate"
                style={{ width: `${Math.round(legitimate_probability * 100)}%` }}
              />
            </div>
            <span>{Math.round(legitimate_probability * 100)}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
