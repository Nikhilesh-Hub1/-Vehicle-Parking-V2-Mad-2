# mails.py
import smtplib
from email.message import EmailMessage
from datetime import datetime
import pytz

# Configuration
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "notifications@parkingapp.com"
IST = pytz.timezone('Asia/Kolkata')

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_email} at {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def daily_reminder_template(user):
    return f"""
Hello {user['name']},

🚗 Parking Reminder ({datetime.now(IST).strftime('%d %b %Y')})

Active Session: {'Yes' if user.get('has_active_session') else 'No'}
Available Spaces: Main Lot ({user.get('spaces',{}).get('main',0)}), West Garage ({user.get('spaces',{}).get('west',0)})

ParkingApp Team
"""

def monthly_summary_template(user):
    return f"""
Hello {user['name']},

📊 Monthly Report ({datetime.now(IST).strftime('%B %Y')})

Sessions: {user.get('total_sessions',0)}
Hours Parked: {user.get('total_hours',0):.1f}
Total Charges: ₹{user.get('amount_spent',0):.2f}

ParkingApp Team
"""