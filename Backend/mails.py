import smtplib
from email.message import EmailMessage
from datetime import datetime
import pytz

# Configuration
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "notifications@parkingapp.com"
IST = pytz.timezone('Asia/Kolkata')

def send_email(to_email, subject, body, html=False):
    msg = EmailMessage()
    if html:
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"[{datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}] Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        raise

