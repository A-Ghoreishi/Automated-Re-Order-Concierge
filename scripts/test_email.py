from src.email_client import send_email, check_inbox
import os

owner = os.getenv("OWNER_EMAIL")

# Send a test email
send_email(owner, "Test Approval Request", "Please reply YES or NO.")

# Check inbox for reply
reply = check_inbox("Test Approval Request")
print("Reply found:", reply)
