"""
Preprocessing utilities.

IMPORTANT: clean_text() below is copied EXACTLY (logic-for-logic) from
Phishing_Email_Detection.ipynb so that predictions at inference time use
the identical text-cleaning pipeline used to train the model. Do not
change this function unless you also retrain the model.
"""

import re


def combine_subject_and_body(subject: str, body: str) -> str:
    """
    Reproduces the notebook step:
        df['subject'] = df['subject'].fillna('')
        df['body'] = df['body'].fillna('')
        df['email_text'] = df['subject'] + ' ' + df['body']
    """
    subject = subject or ""
    body = body or ""
    return f"{subject} {body}"


def clean_text(text: str) -> str:
    """
    Copied exactly from the notebook's clean_text() function.
    """
    text = str(text).lower()

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Keep only letters and spaces
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_email(subject: str, body: str) -> str:
    """Full inference-time preprocessing: combine then clean."""
    return clean_text(combine_subject_and_body(subject, body))
