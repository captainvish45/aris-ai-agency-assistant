from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=200)
    phone: str = Field(..., min_length=7, max_length=50)
    email: EmailStr
    business_name: str = Field(..., min_length=2, max_length=255)
    business_type: str = Field(..., min_length=2, max_length=200)
    monthly_revenue: str = Field(..., min_length=1, max_length=100)
    monthly_marketing_budget: str = Field(..., min_length=1, max_length=100)
    project_budget: str = Field(..., min_length=1, max_length=100)
    service_needed: str = Field(..., min_length=2, max_length=200)


class LeadUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=200)
    phone: Optional[str] = Field(None, min_length=7, max_length=50)
    email: Optional[EmailStr] = None
    business_name: Optional[str] = Field(None, min_length=2, max_length=255)
    business_type: Optional[str] = Field(None, min_length=2, max_length=200)
    monthly_revenue: Optional[str] = Field(None, min_length=1, max_length=100)
    monthly_marketing_budget: Optional[str] = Field(None, min_length=1, max_length=100)
    project_budget: Optional[str] = Field(None, min_length=1, max_length=100)
    service_needed: Optional[str] = Field(None, min_length=2, max_length=200)
    status: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    last_contact_date: Optional[date] = None


class LeadResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: str
    business_name: str
    business_type: str
    monthly_revenue: str
    monthly_marketing_budget: str
    project_budget: str
    service_needed: str
    status: str
    notes: str
    follow_up_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AdminLogin(BaseModel):
    username: str
    password: str


class DashboardStats(BaseModel):
    total_leads: int
    new_leads: int
    contacted_leads: int
    closed_leads: int
    leads_by_service: dict
    leads_by_status: dict
    recent_leads: list[LeadResponse]
