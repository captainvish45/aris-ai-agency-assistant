from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.init_db import init_database
from app.routers import admin, chat, export, public

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(
    title="ARIS AI Agency Assistant",
    description="AI Automation Agency lead capture and management platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(public.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(export.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if (
        exc.status_code == 401
        and request.url.path.startswith("/admin")
        and not request.url.path.endswith("/login")
        and "text/html" in request.headers.get("accept", "")
    ):
        return RedirectResponse(url="/admin/login", status_code=303)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": "ARIS AI Agency Assistant"}
