from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.auth import create_access_token, verify_password
from app.config import LEAD_STATUSES, SERVICE_OPTIONS, SESSION_COOKIE_NAME
from app.database import get_db
from app.dependencies import get_current_admin
from app.models import Admin, Lead
from app.schemas import DashboardStats, LeadResponse, LeadUpdate

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent.parent / "templates"))


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request, "error": None})


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    admin = db.query(Admin).filter(Admin.username == username.strip()).first()
    if not admin or not verify_password(password, admin.hashed_password):
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "error": "Invalid username or password."},
            status_code=401,
        )

    token = create_access_token({"sub": str(admin.id), "username": admin.username})
    response = RedirectResponse(url="/admin/dashboard", status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
    search: str = Query(""),
    status_filter: str = Query(""),
    service_filter: str = Query(""),
):
    query = db.query(Lead)

    if search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Lead.full_name.ilike(term),
                Lead.email.ilike(term),
                Lead.phone.ilike(term),
                Lead.business_name.ilike(term),
            )
        )

    if status_filter and status_filter in LEAD_STATUSES:
        query = query.filter(Lead.status == status_filter)

    if service_filter and service_filter in SERVICE_OPTIONS:
        query = query.filter(Lead.service_needed == service_filter)

    leads = query.order_by(Lead.created_at.desc()).all()

    stats = DashboardStats(
        total_leads=db.query(func.count(Lead.id)).scalar() or 0,
        new_leads=db.query(func.count(Lead.id)).filter(Lead.status == "new").scalar() or 0,
        contacted_leads=db.query(func.count(Lead.id)).filter(Lead.status == "contacted").scalar() or 0,
        closed_leads=db.query(func.count(Lead.id)).filter(Lead.status == "closed").scalar() or 0,
        leads_by_service={},
        leads_by_status={},
        recent_leads=[],
    )

    service_counts = (
        db.query(Lead.service_needed, func.count(Lead.id))
        .group_by(Lead.service_needed)
        .all()
    )
    stats.leads_by_service = {service: count for service, count in service_counts}

    status_counts = (
        db.query(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
        .all()
    )
    stats.leads_by_status = {s: count for s, count in status_counts}

    recent = db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()
    stats.recent_leads = [LeadResponse.model_validate(l) for l in recent]

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "admin": admin,
            "leads": leads,
            "stats": stats,
            "search": search,
            "status_filter": status_filter,
            "service_filter": service_filter,
            "statuses": LEAD_STATUSES,
            "services": SERVICE_OPTIONS,
        },
    )


@router.get("/leads/{lead_id}", response_class=HTMLResponse)
async def lead_detail_page(
    request: Request,
    lead_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    return templates.TemplateResponse(
        "admin/lead_detail.html",
        {
            "request": request,
            "admin": admin,
            "lead": lead,
            "statuses": LEAD_STATUSES,
            "services": SERVICE_OPTIONS,
        },
    )


@router.post("/leads/{lead_id}/update")
async def update_lead(
    lead_id: int,
    request: Request,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    form = await request.form()
    lead.full_name = form.get("full_name", lead.full_name).strip()
    lead.phone = form.get("phone", lead.phone).strip()
    lead.email = form.get("email", lead.email).strip()
    lead.business_name = form.get("business_name", lead.business_name).strip()
    lead.business_type = form.get("business_type", lead.business_type).strip()
    lead.monthly_revenue = form.get("monthly_revenue", lead.monthly_revenue).strip()
    lead.monthly_marketing_budget = form.get("monthly_marketing_budget", lead.monthly_marketing_budget).strip()
    lead.service_needed = form.get("service_needed", lead.service_needed).strip()
    lead.status = form.get("status", lead.status).strip()
    lead.notes = form.get("notes", lead.notes or "").strip()

    follow_up = form.get("follow_up_date", "")
    last_contact = form.get("last_contact_date", "")

    lead.follow_up_date = datetime.strptime(follow_up, "%Y-%m-%d").date() if follow_up else None
    lead.last_contact_date = datetime.strptime(last_contact, "%Y-%m-%d").date() if last_contact else None
    lead.updated_at = datetime.now(timezone.utc)

    db.commit()
    return RedirectResponse(url=f"/admin/leads/{lead_id}?saved=1", status_code=303)


@router.post("/leads/{lead_id}/delete")
async def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(lead)
    db.commit()
    return RedirectResponse(url="/admin/dashboard?deleted=1", status_code=303)


@router.get("/api/stats")
async def get_stats(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    service_counts = (
        db.query(Lead.service_needed, func.count(Lead.id))
        .group_by(Lead.service_needed)
        .all()
    )
    status_counts = (
        db.query(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
        .all()
    )
    return {
        "total": db.query(func.count(Lead.id)).scalar() or 0,
        "new": db.query(func.count(Lead.id)).filter(Lead.status == "new").scalar() or 0,
        "contacted": db.query(func.count(Lead.id)).filter(Lead.status == "contacted").scalar() or 0,
        "closed": db.query(func.count(Lead.id)).filter(Lead.status == "closed").scalar() or 0,
        "by_service": {s: c for s, c in service_counts},
        "by_status": {s: c for s, c in status_counts},
    }
