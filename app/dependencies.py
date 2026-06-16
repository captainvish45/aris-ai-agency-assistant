from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth import decode_access_token
from app.config import SESSION_COOKIE_NAME
from app.database import get_db
from app.models import Admin


def get_current_admin(request: Request, db: Session = Depends(get_db)) -> Admin:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session payload",
        )

    admin = db.query(Admin).filter(Admin.id == int(admin_id)).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin not found",
        )
    return admin


def get_optional_admin(request: Request, db: Session = Depends(get_db)) -> Admin | None:
    try:
        return get_current_admin(request, db)
    except HTTPException:
        return None
