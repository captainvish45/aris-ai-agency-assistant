from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Integer, String, Text

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    business_name = Column(String(255), nullable=False)
    business_type = Column(String(200), nullable=False)
    monthly_revenue = Column(String(100), nullable=False)
    monthly_marketing_budget = Column(String(100), nullable=False)
    project_budget = Column(String(100), nullable=False)
    service_needed = Column(String(200), nullable=False)
    status = Column(String(50), default="new", nullable=False, index=True)
    notes = Column(Text, default="", nullable=False)
    follow_up_date = Column(Date, nullable=True)
    last_contact_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
