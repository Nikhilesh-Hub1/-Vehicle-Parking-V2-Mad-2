# tasks.py
from celery import Celery
from celery.schedules import crontab
import pytz
from mails import send_email, daily_reminder_template, monthly_summary_template

# Initialize Celery
app = Celery('parking_tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# Timezone configuration
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'

# Sample data
def get_daily_users():
    return [{
        'name': 'John Doe',
        'email': 'john@example.com',
        'has_active_session': True,
        'spaces': {'main': 12, 'west': 5}
    }]

def get_monthly_users():
    return [{
        'name': 'John Doe',
        'email': 'john@example.com',
        'total_sessions': 8,
        'total_hours': 24.5,
        'amount_spent': 735.00
    }]

# Celery Tasks
@app.task
def send_daily_reminders():
    """8:00 AM IST daily"""
    for user in get_daily_users():
        send_email(
            user['email'],
            "🚗 Daily Parking Update",
            daily_reminder_template(user)
        )

@app.task
def send_monthly_reports():
    """9:00 AM IST on 1st of month"""
    for user in get_monthly_users():
        send_email(
            user['email'],
            "📊 Monthly Parking Report",
            monthly_summary_template(user)
        )

# Scheduled Tasks (timezone now handled by app config)
app.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=11, minute=35),  # Uses app timezone
    },
    'monthly-reports': {
        'task': 'tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=23, hour=11, minute=36),
    }
}