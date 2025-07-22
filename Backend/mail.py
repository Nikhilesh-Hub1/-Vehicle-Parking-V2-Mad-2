import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from app import app
from models import User 

# Email Configuration
SMTP_SERVER = "localhost"
SMTP_PORT = 1025
FROM_EMAIL = "notifications@parkingapp.com"

def send_email(to_email, subject, body):
    """Send email using MailHog"""
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")

# Parking Reminders
def send_daily_parking_reminders():
    """Send daily parking updates to all users"""
    today = datetime.now().date()
    for user in User.query.all():
        # active_session = ParkingSession.query.filter_by(
        #     user_id=user.id,
        #     end_time=None
        # ).first()

    # if active_session:
        # Active parking reminder
        # body = (
        #     f"Hello {user.name},\n\n"
        #     f"Your vehicle at {active_session.spot.location} has been parked since "
        #     f"{active_session.start_time.strftime('%I:%M %p')}.\n\n"
        #     "Please remember to move it before the time limit expires!"
        # )
        # send_email(user.email, "🚗 Active Parking Reminder", body)
    # else:
        # General parking update
        body = (
            f"Hello {user.name},\n\n"
            "Today's parking availability:\n"
            "- Main Lot: 12 spaces available\n"
            "- West Garage: 5 spaces available\n\n"
            "Have a great day!"
        )
        send_email(user.email, "🅿️ Daily Parking Update", body)

def send_monthly_parking_summary():
    """Send monthly parking reports"""
    month_name = datetime.now().strftime('%B')
    for user in User.query.all():
#         sessions = ParkingSession.query.filter(
#             ParkingSession.user_id == user.id,
#             ParkingSession.start_time >= datetime.now().replace(day=1)
#         ).all()

#         total_hours = sum(
#             (s.end_time or datetime.now() - s.start_time).total_seconds()/3600
#             for s in sessions
#         )

        body = (
            f"Hello {user.name},\n\n"
            # f"Your {month_name} parking summary:\n"
            # f"- Total sessions: {len(sessions)}\n"
            # f"- Total hours parked: {total_hours:.1f}\n"
            # f"- Estimated charges: ${total_hours * 3.5:.2f}\n\n"
            "Thank you for using our parking services!"
        )
        send_email(user.email, f"📊 {month_name} Parking Report", body)

# Job Completion Notifications
# def notify_job_completion(job_id):
#     """Send notification when an export job finishes"""
#     job = ExportJob.query.get(job_id)
#     if not job:
#         print(f"✗ Job {job_id} not found")
#         return

#     status = "completed successfully" if job.success else "failed"
#     body = (
#         f"Export Job Notification\n\n"
#         f"Job ID: {job.id}\n"
#         f"Type: {job.job_type}\n"
#         f"Status: {status}\n"
#         f"Duration: {job.duration:.2f} seconds\n"
#         f"Records processed: {job.records_processed or 0}\n\n"
#         f"Message: {job.message or 'No additional details'}"
#     )

#     # Send to job owner and admins
#     recipients = [job.initiated_by.email]
#     recipients += [admin.email for admin in User.query.filter_by(is_admin=True).all()]
    
#     for email in set(recipients):  # Avoid duplicates
#         send_email(
#             email,
#             f"Export Job {job.id} - {job.status.upper()}",
#             body
#         )

def generate_user_report(user):
    """Create simple text report for a user"""
    last_month = datetime.now().replace(day=1) - timedelta(days=1)
    sessions = ParkingSession.query.filter(
        ParkingSession.user_id == user.id,
        ParkingSession.start_time >= last_month.replace(day=1)
    ).all()
    
    return f"""
{user.name}'s Monthly Parking Report:
----------------------------------
Total Bookings: {len(sessions)}
Favorite Spot: {max((s.spot.location for s in sessions), key=lambda x: x.count())}
Total Spent: ${sum(s.cost for s in sessions):.2f}
----------------------------------
"""


















# Main Execution
if __name__ == "__main__":
    print("Starting notification system...")
    
    # Daily reminders (run every day)
    # send_daily_parking_reminders()
    
    # Monthly summary (run on 1st of month)
    # if datetime.now().day == 1:
    send_monthly_parking_summary()
    
    # Example job notification (would typically be called from your job processor)
    # notify_job_completion(123)  # Uncomment with real job ID
    
    print(f"Check emails at http://localhost:8025")