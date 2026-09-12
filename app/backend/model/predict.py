"""
Loads the trained TF-IDF vectorizer + Logistic Regression model produced
by train_model.py, and exposes a single PhishingModel class whose
predict() mirrors the notebook's exact prediction process:

    subject, body -> email_text -> clean_text -> tfidf.transform -> model.predict / predict_proba
"""

from pathlib import Path

import joblib

from model.preprocessing import preprocess_email

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
VECTORIZER_PATH = ARTIFACTS_DIR / "tfidf_vectorizer.pkl"
MODEL_PATH = ARTIFACTS_DIR / "phishing_model.pkl"

# Matches the notebook's label convention: label 1 = phishing, label 0 = legitimate
LABEL_MAP = {0: "legitimate", 1: "phishing"}


class PhishingModel:
    """Thin wrapper that loads artifacts once and serves predictions."""

    def __init__(self):
        self._vectorizer = None
        self._model = None
        self._loaded = False

    def load(self):
        if not VECTORIZER_PATH.exists() or not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model artifacts not found. From the backend/ directory, run "
                "`python -m model.train_model` first to generate "
                f"{VECTORIZER_PATH.name} and {MODEL_PATH.name}."
            )
        self._vectorizer = joblib.load(VECTORIZER_PATH)
        self._model = joblib.load(MODEL_PATH)
        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict(self, subject: str, body: str) -> dict:
        if not self._loaded:
            raise RuntimeError("Model is not loaded. Call load() first.")

        clean = preprocess_email(subject, body)
        features = self._vectorizer.transform([clean])

        prediction = int(self._model.predict(features)[0])
        probabilities = self._model.predict_proba(features)[0]

        # class order in predict_proba follows model.classes_ (typically [0, 1])
        class_to_index = {cls: i for i, cls in enumerate(self._model.classes_)}
        legitimate_prob = float(probabilities[class_to_index.get(0, 0)])
        phishing_prob = float(probabilities[class_to_index.get(1, 1)])

        return {
            "label": LABEL_MAP.get(prediction, str(prediction)),
            "is_phishing": prediction == 1,
            "phishing_probability": round(phishing_prob, 4),
            "legitimate_probability": round(legitimate_prob, 4),
        }


# Singleton instance used by the FastAPI app
phishing_model = PhishingModel()
