import os, smtplib, imaplib, email
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("EMAIL_HOST")
SMTP_PORT = int(os.getenv("EMAIL_PORT", "587"))
IMAP_HOST = os.getenv("EMAIL_IMAP")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email(to_address: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = EMAIL_USER
    msg["To"] = to_address
    msg["Subject"] = subject

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [to_address], msg.as_string())
    print(f"📧 Email sent to {to_address}")


def check_inbox(subject_filter: str = None):
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    criteria = '(UNSEEN)'
    if subject_filter:
        criteria = f'(UNSEEN SUBJECT "{subject_filter}")'

    status, messages = mail.search(None, criteria)
    if status != "OK":
        return None

    ids = messages[0].split()
    if not ids:
        return None

    latest_id = ids[-1]
    status, data = mail.fetch(latest_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    mail.store(latest_id, "+FLAGS", "\\Seen")
    mail.logout()
    return body.strip()
