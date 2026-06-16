from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import SERVICE_OPTIONS
from app.database import get_db
from app.models import Lead
from app.schemas import LeadCreate, LeadResponse
from app.utils.validators import (
    validate_email,
    validate_phone,
    validate_required,
    validate_service,
)

router = APIRouter(prefix="/api/chat", tags=["chat"])

CHAT_STEPS = [
    {
        "key": "full_name",
        "question": "Welcome to ARIS AI! I'm your agency assistant. Let's get started — what's your full name?",
        "field": "Full Name",
        "type": "text",
    },
    {
        "key": "phone",
        "question": "Great! What's the best phone number to reach you?",
        "field": "Phone Number",
        "type": "tel",
    },
    {
        "key": "email",
        "question": "Perfect. What's your email address?",
        "field": "Email Address",
        "type": "email",
    },
    {
        "key": "business_name",
        "question": "What's the name of your business?",
        "field": "Business Name",
        "type": "text",
    },
    {
        "key": "business_type",
        "question": "What type of business do you operate? (e.g., E-commerce, SaaS, Agency, Local Service)",
        "field": "Business Type",
        "type": "text",
    },
    {
        "key": "monthly_revenue",
        "question": "What is your approximate monthly business revenue? (e.g., ₹50,000 - ₹2,00,000)",
        "field": "Monthly Revenue",
        "type": "text",
    },
    {
        "key": "monthly_marketing_budget",
        "question": "What is your monthly budget for AI automation or marketing?",
        "field": "Monthly Budget",
        "type": "text",
    }, 
    {
        "key": "service_needed",
        "question": "Which AI service are you most interested in?",
        "field": "Service Needed",
        "type": "select",
        "options": SERVICE_OPTIONS,
    },
    {
    "key": "project_budget",
    "question": "What is your project budget?",
    "field": "Project Budget",
    "type": "select",
    "options": [
        "₹5,000 - ₹10,000",
        "₹10,000 - ₹25,000",
        "₹25,000 - ₹50,000",
        "₹50,000 - ₹1,00,000",
        "₹1,00,000+",
        "Custom Budget"
    ],
},
]


def validate_step(key: str, value: str) -> tuple[bool, str]:
    if key == "full_name":
        return validate_required(value, "Full name")
    if key == "phone":
        return validate_phone(value)
    if key == "email":
        return validate_email(value)
    if key == "business_name":
        return validate_required(value, "Business name")
    if key == "business_type":
        return validate_required(value, "Business type")
    if key == "monthly_revenue":
        return validate_required(value, "Monthly revenue", min_length=1)
    if key == "monthly_marketing_budget":
        return validate_required(value, "Monthly marketing budget", min_length=1)
    if key == "service_needed":
        return validate_service(value, SERVICE_OPTIONS)
    return True, ""


@router.get("/steps")
async def get_chat_steps():
    return {"steps": CHAT_STEPS, "total_steps": len(CHAT_STEPS)}


@router.post("/validate")
async def validate_field(payload: dict):
    key = payload.get("key", "")
    value = payload.get("value", "")
    step = next((s for s in CHAT_STEPS if s["key"] == key), None)
    if not step:
        raise HTTPException(status_code=400, detail="Invalid field key")
    valid, message = validate_step(key, value)
    return {"valid": valid, "message": message}


@router.post("/submit", response_model=LeadResponse)
async def submit_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    for step in CHAT_STEPS:
        value = getattr(lead_data, step["key"])
        valid, message = validate_step(step["key"], value)
        if not valid:
            raise HTTPException(status_code=422, detail=message)

    lead = Lead(**lead_data.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
