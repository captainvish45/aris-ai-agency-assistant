# ARIS AI Agency Assistant

A production-ready SaaS application for AI automation agencies to capture, qualify, manage, and track client leads through a conversational AI assistant and powerful admin dashboard.

## Features

- **Landing Page** — Premium dark-themed marketing site with glassmorphism design
- **AI Chat Assistant** — Conversational lead capture with 8-step qualification flow
- **Lead Management** — Search, filter, edit, delete, status tracking, notes, and follow-up dates
- **Admin Dashboard** — Statistics, charts, and full lead pipeline visibility
- **Export Tools** — CSV export and downloadable lead reports
- **Secure Authentication** — JWT-based admin sessions with bcrypt password hashing

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Templates:** Jinja2
- **Charts:** Chart.js

## Quick Start

### 1. Navigate to project directory

```bash
cd aris-ai-agency-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn main:app --reload
```

### 4. Open in browser

| Page | URL |
|------|-----|
| Landing Page | http://127.0.0.1:8000 |
| AI Chat | http://127.0.0.1:8000/chat |
| Admin Login | http://127.0.0.1:8000/admin/login |
| Health Check | http://127.0.0.1:8000/health |

## Default Admin Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

Change these in production by setting environment variables:

```bash
set ADMIN_USERNAME=your_username
set ADMIN_PASSWORD=your_secure_password
set SECRET_KEY=your-secret-key-here
```

## Project Structure

```
aris-ai-agency-assistant/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── aris.db                 # SQLite database (auto-created)
├── app/
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database connection
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication utilities
│   ├── dependencies.py     # FastAPI dependencies
│   ├── init_db.py          # Database initialization
│   ├── routers/
│   │   ├── public.py       # Landing & public pages
│   │   ├── chat.py         # Chat API endpoints
│   │   ├── admin.py        # Admin dashboard routes
│   │   └── export.py       # Export functionality
│   └── utils/
│       └── validators.py   # Input validation
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── chat.html
│   ├── success.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       └── lead_detail.html
└── static/
    ├── css/main.css
    └── js/
        ├── main.js
        ├── chat.js
        └── dashboard.js
```

## Chat Flow

The AI assistant collects the following information:

1. Full Name
2. Phone Number
3. Email Address
4. Business Name
5. Business Type
6. Monthly Revenue
7. Monthly Marketing Budget
8. Service Needed (select from 8 AI services)

After collection, users review a summary, confirm, and the lead is saved to the database.

## Admin Dashboard

- **Statistics:** Total, new, contacted, and closed leads
- **Charts:** Leads by status (doughnut) and by service (bar)
- **Lead Table:** Searchable and filterable lead list
- **Lead Details:** Edit all fields, change status, add notes, set follow-up dates
- **Export:** Download CSV or full text report

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/steps` | Get chat conversation steps |
| POST | `/api/chat/validate` | Validate a single field |
| POST | `/api/chat/submit` | Submit completed lead |
| GET | `/admin/api/stats` | Dashboard statistics (auth required) |
| GET | `/admin/export/csv` | Export leads as CSV (auth required) |
| GET | `/admin/export/report` | Download lead report (auth required) |

## Database Schema

### `leads` table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| full_name | VARCHAR | Client full name |
| phone | VARCHAR | Phone number |
| email | VARCHAR | Email address |
| business_name | VARCHAR | Business name |
| business_type | VARCHAR | Type of business |
| monthly_revenue | VARCHAR | Monthly revenue range |
| monthly_marketing_budget | VARCHAR | Marketing budget |
| service_needed | VARCHAR | Selected AI service |
| status | VARCHAR | new / contacted / closed |
| notes | TEXT | Admin notes |
| follow_up_date | DATE | Scheduled follow-up |
| last_contact_date | DATE | Last contact date |
| created_at | DATETIME | Record creation time |
| updated_at | DATETIME | Last update time |

### `admins` table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | VARCHAR | Login username |
| email | VARCHAR | Admin email |
| hashed_password | VARCHAR | Bcrypt hash |
| created_at | DATETIME | Account creation time |

## License

MIT License — Free to use and modify for your AI automation agency.
