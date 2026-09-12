"""
FastAPI backend for the Phishing Email Detection app.

Endpoints:
    GET  /            -> basic info
    GET  /health       -> health check + whether the model is loaded
    POST /predict      -> run a subject/body pair through the trained
                           TF-IDF + Logistic Regression pipeline

Run locally (from the backend/ directory):
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from model.predict import phishing_model
from utils.schemas import EmailInput, HealthResponse, PredictionResponse

app = FastAPI(
    title="Phishing Email Detection API",
    description=(
        "Detects whether an email is phishing or legitimate using a "
        "TF-IDF + Logistic Regression pipeline trained on subject/body text."
    ),
    version="1.0.0",
)

# Allow the Vite dev server (and any frontend) to call this API.
# For production, replace "*" with your deployed frontend's exact origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_model_on_startup():
    try:
        phishing_model.load()
        print("Model and vectorizer loaded successfully.")
    except FileNotFoundError as exc:
        # Don't crash the server — /predict will return a clear error
        # until the user runs the training script.
        print(f"WARNING: {exc}")


@app.get("/", tags=["Info"])
def root():
    return {
        "message": "Phishing Email Detection API",
        "docs": "/docs",
        "predict_endpoint": "/predict",
    }


@app.get("/health", response_model=HealthResponse, tags=["Info"])
def health():
    return HealthResponse(status="ok", model_loaded=phishing_model.is_loaded)


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(payload: EmailInput):
    if not phishing_model.is_loaded:
        raise HTTPException(
            status_code=503,
            detail=(
                "Model is not loaded. From the backend/ directory, run "
                "`python -m model.train_model` to generate the model artifacts, "
                "then restart the server."
            ),
        )

    try:
        result = phishing_model.predict(payload.subject, payload.body)
    except Exception as exc:  # defensive: never leak stack traces to the client
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return PredictionResponse(**result)


@app.exception_handler(ValidationError)
def validation_exception_handler(request, exc):
    raise HTTPException(status_code=422, detail=exc.errors())
