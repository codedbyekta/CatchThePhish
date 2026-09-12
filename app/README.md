# Phishing Email Detector

A full-stack app that classifies an email's subject + body as **phishing**
or **legitimate**, built around the model developed in
[`Phishing_Email_Detection.ipynb`](https://github.com/codedbyekta/AI-Model-Lab/blob/main/Phishing_Email_Detection.ipynb).

This is a **separate, standalone application** — it does not share code,
dependencies, or ports with any other model app in this repo/portfolio.

```
app/
├── frontend/     React + Vite UI
├── backend/      FastAPI + Pydantic API
└── README.md     you are here
```

---

## 1. Project overview

You paste an email's subject and body into a simple web form. The React
frontend sends that text to a FastAPI backend, which runs it through the
same text-cleaning pipeline used in the notebook, feeds it into a
TF-IDF vectorizer + Logistic Regression classifier, and returns a
prediction (`phishing` / `legitimate`) with a confidence score.

---

## 2. The model (from the notebook)

The notebook trains and compares three models — Logistic Regression,
Random Forest, and XGBoost (on SVD-reduced features) — on a labeled
email dataset (`subject`, `body`, `label`, where `label 1 = phishing`,
`label 0 = legitimate`). It later uses **Logistic Regression** as the
reference model for feature-importance and adversarial-evasion analysis,
and it's also the strongest, simplest, most explainable of the three
(97.62% accuracy / 97.31% F1 in the notebook's run). That's the model
this app deploys.

**Exact pipeline reproduced from the notebook:**

1. Fill missing `subject`/`body` with `""`.
2. Combine: `email_text = subject + " " + body`.
3. `clean_text()` — lowercase, strip HTML tags, strip URLs, strip email
   addresses, keep only letters and spaces, collapse whitespace. Copied
   logic-for-logic from the notebook into `backend/model/preprocessing.py`.
4. `TfidfVectorizer(max_features=10000, ngram_range=(1,2), min_df=2, max_df=0.95, sublinear_tf=True)`.
5. `LogisticRegression(max_iter=1000, random_state=42)`.
6. Prediction: `model.predict()` for the label, `model.predict_proba()`
   for the confidence.

**Important — no pre-trained artifacts existed to reuse.** The notebook
never calls `joblib.dump`/`pickle.dump`, and the dataset file
(`meajor_cleaned_preprocessed.csv`) isn't committed to the repo. So there
was nothing to "load as-is." Instead, `backend/model/train_model.py`
reproduces the exact pipeline above and fits it fresh, saving the
vectorizer and model as `.pkl` files that the API loads at startup.

**About the bundled demo dataset:** so the app works out of the box, a
tiny synthetic dataset (`backend/model/data/generate_demo_dataset.py`)
is generated automatically if no real dataset is present. It is **not**
your real dataset and will **not** reproduce the notebook's 97.62%
accuracy — it exists only to prove the pipeline runs end-to-end. To get
real results:

```bash
# Put your real CSV here (must have columns: subject, body, label)
cp /path/to/meajor_cleaned_preprocessed.csv backend/model/data/

cd backend
python -m model.train_model
```

This retrains on your real data and overwrites the demo artifacts —
no model logic changes, only the data it's fit on.

---

## 3. Architecture

```
┌─────────────────┐        POST /predict         ┌──────────────────────┐
│  React (Vite)    │  {subject, body}  ────────▶  │  FastAPI              │
│  frontend/       │                              │  backend/main.py      │
│                  │  ◀──────────────────────────  │                       │
│  EmailForm       │   {label, is_phishing,       │  Pydantic validation  │
│  ResultCard      │    phishing_probability,     │  clean_text()         │
│                  │    legitimate_probability}   │  TF-IDF transform     │
└─────────────────┘                              │  LogisticRegression   │
                                                   │  .pkl artifacts       │
                                                   └──────────────────────┘
```

- **No database.** Every request is stateless — text in, prediction out.
  The model doesn't need persisted user data, so none is used.
- **No authentication.** This is a single-purpose classifier tool with
  no user accounts or private data to protect.

---

## 4. Frontend ↔ backend flow

1. User types/pastes a subject (optional) and body (required) into the form.
2. On submit, `src/api.js` POSTs `{ subject, body }` to `${VITE_API_BASE_URL}/predict`.
3. While waiting, the UI shows a loading state; on failure it shows a
   readable error message (network error, validation error, or server error).
4. On success, `ResultCard` shows **Likely Phishing** / **Likely Legitimate**,
   the confidence percentage, and a small probability bar for each class.

---

## 5. API reference

### `POST /predict`

**Request body:**

```json
{
  "subject": "Urgent: Verify your account immediately",
  "body": "Dear customer, click the link below immediately to verify your account or it will be suspended."
}
```

- `subject` — optional string, max 2000 chars.
- `body` — required non-empty string, max 20000 chars.

**Response:**

```json
{
  "label": "phishing",
  "is_phishing": true,
  "phishing_probability": 0.9063,
  "legitimate_probability": 0.0937
}
```

**Error responses:**
- `422` — validation error (e.g. missing/blank `body`), with FastAPI's
  standard `detail` array.
- `503` — model artifacts not found (run the training script first).
- `500` — unexpected prediction failure (message included, no stack trace leaked).

### `GET /health`
Returns `{ "status": "ok", "model_loaded": true|false }`.

### `GET /`
Basic info + links to `/docs` (interactive Swagger UI, auto-generated by FastAPI).

---

## 6. Setup instructions

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Backend

```bash
cd app/backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Train the model (generates a demo dataset automatically if you
# haven't supplied your real one — see section 2 above)
python -m model.train_model
```

### Frontend

```bash
cd app/frontend
npm install
cp .env.example .env    # adjust VITE_API_BASE_URL if needed
```

---

## 7. Running locally

**Terminal 1 — backend:**
```bash
cd app/backend
uvicorn main:app --reload --port 8000
```
API docs at http://localhost:8000/docs

**Terminal 2 — frontend:**
```bash
cd app/frontend
npm run dev
```
App at http://localhost:5173

Open the frontend, paste an email's subject/body, and click **Check Email**.

---

## 8. Deployment

This app has no database and no auth, so deployment is just "run the
backend somewhere, run the frontend somewhere, point one at the other."

### Backend
Any Python host that can run a Uvicorn/ASGI app works (Render, Railway,
Fly.io, a VM, a container, etc.).

```bash
# Production-style run (no --reload)
uvicorn main:app --host 0.0.0.0 --port 8000
```

Make sure `backend/model/artifacts/*.pkl` exist before starting the
server in production — either commit them (if trained on your real,
non-sensitive dataset) or run `python -m model.train_model` as a build
step.

In `main.py`, tighten CORS before going to production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    ...
)
```

### Frontend
Any static host works (Vercel, Netlify, Cloudflare Pages, GitHub Pages, etc.).

```bash
cd app/frontend
npm run build      # outputs to frontend/dist/
```
Set `VITE_API_BASE_URL` in your hosting provider's environment variables
to your deployed backend's URL, then deploy the `dist/` folder (or let
the platform build it directly from the repo).

---

## 9. What was intentionally NOT changed

- No new model logic, features, or hyperparameters were introduced —
  `clean_text()`, the TF-IDF settings, and the Logistic Regression
  settings are copied exactly from the notebook.
- No database was added (the model doesn't need one).
- No authentication was added (not necessary for a single-purpose
  classifier with no user data to protect).
- The notebook's "robust" adversarially-augmented model and the
  Random Forest / XGBoost baselines were **not** deployed — the plain
  Logistic Regression + TF-IDF baseline was chosen as it's the
  strongest, simplest, and most explainable of the three, and the
  one the notebook itself uses as the reference model in later analysis.
