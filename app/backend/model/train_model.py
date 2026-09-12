"""
Reproduces the EXACT baseline pipeline from Phishing_Email_Detection.ipynb:
    load data -> fillna -> combine subject+body -> clean_text ->
    train/test split -> TfidfVectorizer -> LogisticRegression
and saves the fitted vectorizer + model as artifacts the FastAPI backend
loads at startup.

Usage (run from the backend/ directory):
    python -m model.train_model

By default this looks for `model/data/meajor_cleaned_preprocessed.csv`.
If it is not present, a small DEMO dataset is generated first (see
model/data/generate_demo_dataset.py) so you can see the whole app
working end-to-end. Swap in your real dataset (same column names:
subject, body, label) and re-run this script to get production-quality
accuracy matching the notebook.
"""

import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))  # backend/ on path

from model.preprocessing import clean_text  # noqa: E402

DATA_DIR = os.path.join(CURRENT_DIR, "data")
DATASET_PATH = os.path.join(DATA_DIR, "meajor_cleaned_preprocessed.csv")
ARTIFACTS_DIR = os.path.join(CURRENT_DIR, "artifacts")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "phishing_model.pkl")


def ensure_dataset():
    if not os.path.exists(DATASET_PATH):
        print("No dataset found at", DATASET_PATH)
        print("Generating a small DEMO dataset so the pipeline can run end-to-end.")
        print("Replace this file with your real dataset for production results.\n")
        sys.path.append(DATA_DIR)
        from generate_demo_dataset import main as generate_demo  # noqa: E402

        cwd = os.getcwd()
        os.chdir(DATA_DIR)
        try:
            generate_demo()
        finally:
            os.chdir(cwd)


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    ensure_dataset()

    # ---- Load dataset ----
    df = pd.read_csv(DATASET_PATH)
    print("Dataset shape:", df.shape)

    # ---- Handle missing values + combine subject/body ----
    df["subject"] = df["subject"].fillna("")
    df["body"] = df["body"].fillna("")
    df["email_text"] = df["subject"] + " " + df["body"]
    df = df[df["email_text"].str.strip() != ""].copy()

    # ---- Clean text ----
    df["clean_text"] = df["email_text"].apply(clean_text)

    # ---- Clean labels ----
    df = df.dropna(subset=["label"]).copy()
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"]).copy()
    df["label"] = df["label"].astype(int)

    X = df["clean_text"]
    y = df["label"]

    # ---- Train/test split ----
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # ---- TF-IDF vectorization ----
    tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # ---- Logistic Regression ----
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train_tfidf, y_train)

    y_pred = lr_model.predict(X_test_tfidf)

    print("\nLogistic Regression Results")
    print("-" * 30)
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, zero_division=0))
    print("Recall   :", recall_score(y_test, y_pred, zero_division=0))
    print("F1-Score :", f1_score(y_test, y_pred, zero_division=0))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # ---- Save artifacts ----
    joblib.dump(tfidf, VECTORIZER_PATH)
    joblib.dump(lr_model, MODEL_PATH)
    print(f"\nSaved vectorizer to {VECTORIZER_PATH}")
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
