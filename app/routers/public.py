from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.config import SERVICE_OPTIONS

router = APIRouter(tags=["public"])
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse(
        "landing.html",
        {"request": request, "service_options": SERVICE_OPTIONS},
    )


@router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "service_options": SERVICE_OPTIONS},
    )


@router.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    lead_id = request.query_params.get("lead_id", "")
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "lead_id": lead_id},
    )
