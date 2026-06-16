import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'aris.db'}")
SECRET_KEY = os.getenv("SECRET_KEY", "aris-ai-agency-dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SESSION_COOKIE_NAME = "aris_admin_session"
DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
DEFAULT_ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@arisai.com")

SERVICE_OPTIONS = [
    "AI Chatbot",
    "WhatsApp Automation",
    "Appointment Booking Bot",
    "Instagram DM Automation",
    "AI Voice Agent",
]

LEAD_STATUSES = ["new", "contacted", "closed"]
