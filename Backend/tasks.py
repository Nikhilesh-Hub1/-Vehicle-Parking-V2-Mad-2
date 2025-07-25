from celery import Celery
from celery.schedules import crontab
from extensions import db
from models import User, Reservation, ParkingLot, ParkingSpot
from datetime import datetime, timedelta
from mails import send_email
import csv
from io import StringIO
import pytz
from app import create_app 
import os
from time import sleep


# Initialize Celery
app = Celery('parking_tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# Timezone configuration
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'

# Create Flask app instance
flask_app = create_app()

# --- DAILY REMINDER ---
@app.task
def send_daily_reminders():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            # Get all active reservations for the user
            active_reservations = Reservation.query.filter_by(
                user_id=user.id,
                leaving_timestamp=None
            ).all()
            
            if active_reservations:
                # Build reservation details
                reservation_details = ""
                for res in active_reservations:
                    lot = ParkingLot.query.get(res.spot.lot_id)
                    hours = (datetime.utcnow() - res.parking_timestamp).total_seconds() / 3600
                    cost = round(hours * lot.price_per_hour, 2)
                    reservation_details += f"""
                    <li>
                        Lot: {lot.prime_location_name}<br>
                        Spot ID: {res.spot_id}<br>
                        Vehicle: {res.vehicle_number}<br>
                        Since: {res.parking_timestamp.strftime('%Y-%m-%d %H:%M')}<br>
                        Current Cost: ₹{cost}
                    </li>
                    """
                body = f"""
                Hello {user.name},<br><br>
                You currently have {len(active_reservations)} active reservation(s):<br>
                <ul>{reservation_details}</ul>
                <br><em>ParkingApp Team</em>
                """
                subject = "Your Active Parking Reservations" 
            else:
                # No active reservations → show available spots
                lots = ParkingLot.query.all()
                lot_info = ""
                for lot in lots:
                    available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
                    lot_info += f"- {lot.prime_location_name}: {available} available<br>"
                body = f"""
                Hello {user.name},<br><br>
                Don't forget to book your parking spot for tomorrow.<br>
                <strong>Available Spaces:</strong><br>{lot_info}<br>
                <em>ParkingApp Team</em>
                """
            subject = "Daily Parking Reminder"
            send_email(user.email, subject, body, html=True)
           

# # --- MONTHLY SUMMARY ---
@app.task
def send_monthly_reports(end_date=None):
    """
    Sends parking activity reports for all users up to the given date.
    If no date is provided, defaults to current date.
    """
    with flask_app.app_context():
        # If no date provided, use now
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_date = datetime.utcnow()

        # Fetch all users
        users = User.query.all()

        for user in users:
            # Fetch all reservations up to end_date
            reservations = (
                Reservation.query
                .filter(
                    Reservation.user_id == user.id,
                    Reservation.parking_timestamp <= end_date
                )
                .all()
            )
        
            if not reservations:
                continue  # Skip users with no activity

            total_reservations = len(reservations)
            total_spent = sum(r.parking_cost or 0 for r in reservations)

            # Find most used lot
            lot_counts = {}
            for r in reservations:
                lot_name = ParkingLot.query.get(r.spot.lot_id).prime_location_name
                lot_counts[lot_name] = lot_counts.get(lot_name, 0) + 1
            most_used_lot = max(lot_counts, key=lot_counts.get)

            # Build HTML
            body = f"""
            <h2>Parking Activity Report</h2>
            <p>Hello {user.name},</p>
            <p>Here’s a summary of your parking activity until <strong>{end_date.strftime('%Y-%m-%d')}</strong>:</p>
            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                <tr><th>Total Reservations</th><td>{total_reservations}</td></tr>
                <tr><th>Total Spent</th><td>₹{total_spent:.2f}</td></tr>
                <tr><th>Most Used Lot</th><td>{most_used_lot}</td></tr>
            </table>
            <br>
            <p>Thank you for using our service!</p>
            <em>- ParkingApp Team</em>
            """

            # Send email
            send_email(user.email, f"Your Parking Report (Till {end_date.strftime('%Y-%m-%d')})", body, html=True)
# --- CSV EXPORT (USER TRIGGERED) ---
@app.task
def export_reservations_csv(user_id):
    with flask_app.app_context():
        user = User.query.get(user_id)
        if not user:
            return "User not found"
        
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        if not reservations:
            send_email(
                user.email,
                "No Reservations Found",
                f"Hi {user.name},<br>You do not have any reservations to export.<br><br>ParkingApp Team",
                html=True
            )
            return "No reservations"

        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Reservation ID", "Lot Name", "Spot ID", "Vehicle", "Parking Start", "Leaving Time", "Cost (₹)", "Remarks"])
        
        for r in reservations:
            writer.writerow([
                r.id,
                r.spot.lot.prime_location_name,
                r.spot_id,
                r.vehicle_number or "N/A",
                r.parking_timestamp.strftime("%Y-%m-%d %H:%M"),
                r.leaving_timestamp.strftime("%Y-%m-%d %H:%M") if r.leaving_timestamp else "Active",
                r.parking_cost or 0,
                "Ongoing" if r.leaving_timestamp is None else "Completed"
            ])

        # Save file
        save_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"reservations_{user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(save_dir, filename)
        with open(file_path, "w") as f:
            f.write(output.getvalue())

        # Generate download link
        download_url = f"http://127.0.0.1:5000/download/{filename}"
        for i in range (5):
            sleep(2)
            print(f"Exporting CSV....{i+1}/5")
        # Send email with link
        send_email(
            user.email,
            "Your Parking Data Export is Ready",
            f"""
            Hi {user.name},<br><br>
            Your parking data export is ready.<br>
            <a href="{download_url}">Click here to download your file</a>.<br><br>
            <em>ParkingApp Team</em>
            """,
            html=True
        )

        return file_path

@app.task
def export_all_users_csv(admin_id):
     with flask_app.app_context():
        admin = User.query.get(admin_id)
        if not admin or admin.role != 'admin':
            return "Unauthorized"

        users = User.query.all()
        if not users:
            send_email(
                admin.email,
                "No Users Found",
                f"Hi {admin.name},<br>No users found in the system.<br><br>ParkingApp Team",
                html=True
            )
            return "No users found"

        # Prepare CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["User ID", "Name", "Email", "Role"])
        for u in users:
            writer.writerow([u.id, u.name, u.email, u.role])

        # Ensure exports directory exists
        export_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(export_dir, exist_ok=True)
        filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(export_dir, filename)

        with open(filepath, "w") as f:
            f.write(output.getvalue())

        # Send email with download link
        download_url = f"http://127.0.0.1:5000/download/{filename}"
        body = f"""
        Hi {admin.name},<br><br>
        Your users export is ready.<br>
        <a href="{download_url}">Click here to download</a><br><br>
        ParkingApp Team
        """
        for i in range (5):
            sleep(2)
            print(f"Exporting CSV....{i+1}/5")
        send_email(admin.email, "User Data Export Ready", body, html=True)
        return filepath



# Scheduled Tasks configuration
app.conf.beat_schedule = {
    'daily-reminder': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=12, minute=5),  # 8:00 AM IST daily
    },
    'monthly-summary': {
        'task': 'tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=25, hour=12, minute=6),
        'args': (datetime.utcnow().strftime("%Y-%m-%d"),)  
    },
}