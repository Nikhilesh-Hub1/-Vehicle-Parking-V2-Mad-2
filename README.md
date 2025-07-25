# Vehicle Parking App

A multi-user web application for managing 4-wheeler parking lots, spots, and reservations.  
Built with **Flask (backend)**, **Vue 3 (frontend)**, **SQLite**, **Redis**, and **Celery**.

---

## Features

- **Role-based login**: Separate dashboards for Admin and Users.
- **Admin Features**:
  - Manage parking lots and spots.
  - View reservations and export data.
  - Scheduled tasks & caching for performance.
- **User Features**:
  - Search and reserve available parking spots.
  - View booking history and active reservations.
- **Responsive UI** built with **Bootstrap**.
- **Data Export**: Admins can export reservation and user data.
- **Background Jobs** with **Celery** (e.g., auto-updating statuses).

---

## Tech Stack

- **Frontend**: Vue 3 + Bootstrap
- **Backend**: Flask (REST API)
- **Database**: SQLite
- **Caching & Background Tasks**: Redis + Celery
- **Task Scheduling**: Celery Beat

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js + npm
- Redis (for Celery tasks)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/24f100556/Vehicle-Parking-V2-Mad-2.git
cd vehicle-parking-app/backend

# Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run Flask server
flask run

Frontend Setup

cd frontend
npm install
npm run dev


Start Redis & Celery

# Start Redis (make sure it's running)
redis-server

Mailhog

# Start Celery worker
celery -A tasks worker --loglevel=info

# Start Celery beat (if using scheduled tasks)
celery -A tasks beat --loglevel=info

![alt text](<Screenshot 2025-07-25 at 3.35.19 PM.png>)
```
