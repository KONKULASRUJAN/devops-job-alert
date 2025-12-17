import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

RECIPIENT = os.environ.get("RECIPIENT_EMAIL")
SENDER = RECIPIENT
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

QUERIES = [
    'site:careers.google.com "DevOps Engineer"',
    'site:amazon.jobs "DevOps Engineer"',
    'site:careers.microsoft.com "DevOps Engineer"',
    'site:tcs.com/careers "DevOps Engineer"',
    'site:infosys.com/careers "DevOps Engineer"',
    'DevOps Engineer startup hiring'
]

def search(query):
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    return [{
        "title": query,
        "link": url
    }]

def send_email(results):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = f"Daily DevOps Jobs - {datetime.now().date()}"

    body = ""
    for r in results:
        body += f"{r['title']}\n{r['link']}\n\n"

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def main():
    results = []
    for q in QUERIES:
        results.extend(search(q))
    send_email(results)

if __name__ == "__main__":
    main()
