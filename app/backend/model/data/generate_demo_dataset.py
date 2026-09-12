"""
Generates a SMALL DEMO dataset with the same columns as the notebook's
real dataset (subject, body, label) so the training pipeline can be
exercised end-to-end locally without the original
`meajor_cleaned_preprocessed.csv` file.

This is NOT the dataset used in the notebook and will NOT reproduce the
notebook's reported accuracy (97.62%). It exists purely so this app has
something real to train on out of the box. Replace
`meajor_cleaned_preprocessed.csv` in this folder with your real dataset
(same column names: subject, body, label) and re-run train_model.py to
get production-quality results.
"""

import csv
import random

random.seed(42)

phishing_subjects = [
    "Urgent: Verify your account immediately",
    "Your account has been suspended",
    "Action required: confirm your password",
    "You have won a free prize, claim now",
    "Security alert: unusual login detected",
    "Final notice: your payment failed",
    "Congratulations! You are today's winner",
    "Immediate action needed on your account",
    "Your account will be closed in 24 hours",
    "Confirm your identity to avoid suspension",
]

phishing_bodies = [
    "Dear customer, click the link below immediately to verify your account or it will be suspended.",
    "We detected unusual activity on your account. Verify your password now to avoid permanent suspension.",
    "Congratulations, you have won a cash prize. Click here and enter your bank details to claim your reward.",
    "Your payment could not be processed. Update your card information immediately by clicking this link.",
    "This is an urgent security notice. Confirm your login credentials now to keep your account active.",
    "Act now! Your account access will be revoked unless you verify your information within 24 hours.",
    "Click the link and enter your username and password to restore full access to your account.",
    "Your account has been locked for security reasons. Verify your identity immediately to unlock it.",
]

legit_subjects = [
    "Team meeting rescheduled to Thursday",
    "Your monthly newsletter is here",
    "Project update and next steps",
    "Lunch this weekend?",
    "Invoice for your recent purchase",
    "Reminder: submit your timesheet",
    "Notes from today's standup",
    "Welcome to our community",
    "Your order has shipped",
    "Quarterly report attached",
]

legit_bodies = [
    "Hi team, just a reminder that our meeting has been moved to Thursday at 3pm. See you there.",
    "Here is this month's newsletter with updates on our latest projects and community events.",
    "Attached is the project status update along with the next steps we discussed on our last call.",
    "Hey, are you free for lunch this weekend? Let me know what time works for you.",
    "Please find attached the invoice for your recent purchase. Let us know if you have any questions.",
    "This is a friendly reminder to submit your timesheet before the end of the week.",
    "Here are the notes from today's standup meeting for anyone who could not attend.",
    "Welcome aboard! We are excited to have you join our community. Let us know if you need anything.",
    "Good news, your order has shipped and should arrive within 3 to 5 business days.",
    "Attached is the quarterly report for review before Friday's meeting.",
]


def build_rows(subjects, bodies, label, n):
    rows = []
    for _ in range(n):
        subject = random.choice(subjects)
        body = random.choice(bodies)
        rows.append({"subject": subject, "body": body, "label": label})
    return rows


def main():
    rows = build_rows(phishing_subjects, phishing_bodies, 1, 150) + build_rows(
        legit_subjects, legit_bodies, 0, 150
    )
    random.shuffle(rows)

    with open("meajor_cleaned_preprocessed.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["subject", "body", "label"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} demo rows to meajor_cleaned_preprocessed.csv")


if __name__ == "__main__":
    main()
