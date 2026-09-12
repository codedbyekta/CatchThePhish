# CatchThePhish – Phishing Email Detector

A full-stack machine learning application that classifies emails as **phishing** or **legitimate** using their subject and body.

Built using the model developed in [`Phishing_Email_Detection.ipynb`](https://github.com/codedbyekta/AI-Model-Lab/blob/main/Phishing_Email_Detection.ipynb).

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** FastAPI, Pydantic
- **ML:** Python, Scikit-learn, TF-IDF, Logistic Regression

## ML Pipeline

```text
Email Subject + Body
        ↓
Text Preprocessing
        ↓
TF-IDF Vectorization
        ↓
Logistic Regression
        ↓
Phishing / Legitimate
```

The model achieved **97.62% accuracy** and **97.31% F1 score** in the original notebook.

## Features

- Phishing email detection
- Probability/confidence for both classes
- FastAPI REST API
- React web interface
- Swagger API documentation

## Run Locally

### Backend

```bash
cd app/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m model.train_model
python -m uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd app/frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

Backend API: `http://localhost:8000`

Swagger: `http://localhost:8000/docs`

## Dataset

The original training dataset is not included in the repository due to its size. Place `meajor_cleaned_preprocessed.csv` inside:

```text
app/backend/model/data/
```

and run the training command above.

## Project Structure

```text
CatchThePhish/
└── app/
    ├── frontend/
    ├── backend/
    │   ├── model/
    │   └── utils/
    └── README.md
```

## Author

**Ekta**  
B.Tech CSE-AI, IGDTUW
