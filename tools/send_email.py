#!/usr/bin/env python3
"""
Sends the formatted HTML email via Gmail SMTP.
Reads .tmp/formatted_email.html and .tmp/draft.md (for subject).
Usage: python tools/send_email.py [--dry-run] [--subject "Custom subject"]
"""

import os
import re
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

HTML_PATH = Path(".tmp/formatted_email.html")
DRAFT_PATH = Path(".tmp/draft.md")


def extract_subject_from_draft() -> str:
    """Pull the H1 title from the markdown draft as the email subject."""
    if not DRAFT_PATH.exists():
        return "Money Matters — Weekly Newsletter"
    with open(DRAFT_PATH) as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return "Money Matters — Weekly Newsletter"


def send(subject: str, html_body: str, recipients: list[str], dry_run: bool = False):
    sender = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender or not app_password:
        print("ERROR: GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set in .env")
        raise SystemExit(1)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"The Bell <{sender}>"
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    if dry_run:
        print(f"[DRY RUN] Would send '{subject}' to: {', '.join(recipients)}")
        print(f"[DRY RUN] HTML size: {len(html_body)} bytes")
        return

    print(f"Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipients, msg.as_string())

    print(f"Sent '{subject}' to {len(recipients)} recipient(s): {', '.join(recipients)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be sent without actually sending")
    parser.add_argument("--subject", type=str, default=None,
                        help="Override the email subject line")
    args = parser.parse_args()

    if not HTML_PATH.exists():
        print(f"ERROR: {HTML_PATH} not found. Run format_email.py first.")
        raise SystemExit(1)

    with open(HTML_PATH) as f:
        html_body = f.read()

    subject = args.subject or extract_subject_from_draft()

    recipients_env = os.getenv("RECIPIENT_EMAILS", "")
    if not recipients_env:
        print("ERROR: RECIPIENT_EMAILS not set in .env")
        raise SystemExit(1)
    recipients = [r.strip() for r in recipients_env.split(",") if r.strip()]

    send(subject, html_body, recipients, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
