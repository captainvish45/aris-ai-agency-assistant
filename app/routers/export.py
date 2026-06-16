import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.config import LEAD_STATUSES, SERVICE_OPTIONS
from app.database import get_db
from app.dependencies import get_current_admin
from app.models import Admin, Lead

router = APIRouter(prefix="/admin/export", tags=["export"])


def lead_to_row(lead: Lead) -> list:
    return [
        lead.id,
        lead.full_name,
        lead.phone,
        lead.email,
        lead.business_name,
        lead.business_type,
        lead.monthly_revenue,
        lead.monthly_marketing_budget,
        lead.service_needed,
        lead.status,
        lead.notes or "",
        lead.follow_up_date.isoformat() if lead.follow_up_date else "",
        lead.last_contact_date.isoformat() if lead.last_contact_date else "",
        lead.created_at.isoformat() if lead.created_at else "",
        lead.updated_at.isoformat() if lead.updated_at else "",
    ]


HEADERS = [
    "ID",
    "Full Name",
    "Phone",
    "Email",
    "Business Name",
    "Business Type",
    "Monthly Revenue",
    "Monthly Marketing Budget",
    "Service Needed",
    "Status",
    "Notes",
    "Follow Up Date",
    "Last Contact Date",
    "Created At",
    "Updated At",
]


@router.get("/csv")
async def export_csv(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
    status_filter: str = Query(""),
    service_filter: str = Query(""),
):
    query = db.query(Lead)

    if status_filter and status_filter in LEAD_STATUSES:
        query = query.filter(Lead.status == status_filter)

    if service_filter and service_filter in SERVICE_OPTIONS:
        query = query.filter(Lead.service_needed == service_filter)

    leads = query.order_by(Lead.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(HEADERS)
    for lead in leads:
        writer.writerow(lead_to_row(lead))

    output.seek(0)
    filename = f"aris_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/report")
async def export_report(
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin),
):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()

    lines = [
        "ARIS AI Agency Assistant - Lead Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Leads: {len(leads)}",
        "",
        "=" * 60,
        "",
    ]

    for lead in leads:
        lines.extend([
            f"Lead #{lead.id}",
            f"  Name: {lead.full_name}",
            f"  Email: {lead.email}",
            f"  Phone: {lead.phone}",
            f"  Business: {lead.business_name} ({lead.business_type})",
            f"  Revenue: {lead.monthly_revenue}",
            f"  Marketing Budget: {lead.monthly_marketing_budget}",
            f"  Service: {lead.service_needed}",
            f"  Status: {lead.status.upper()}",
            f"  Notes: {lead.notes or 'N/A'}",
            f"  Follow Up: {lead.follow_up_date or 'N/A'}",
            f"  Last Contact: {lead.last_contact_date or 'N/A'}",
            f"  Created: {lead.created_at.strftime('%Y-%m-%d %H:%M') if lead.created_at else 'N/A'}",
            "-" * 40,
            "",
        ])

    content = "\n".join(lines)
    filename = f"aris_lead_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    return StreamingResponse(
        iter([content]),
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
