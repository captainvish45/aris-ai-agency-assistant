from app.config import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_USERNAME,
)
from app.database import Base, SessionLocal, engine
from app.models import Admin
from app.auth import get_password_hash, verify_password


def init_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = Admin(
                username=DEFAULT_ADMIN_USERNAME,
                email=DEFAULT_ADMIN_EMAIL,
                hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
            )
            db.add(admin)
            db.commit()
        elif not verify_password(DEFAULT_ADMIN_PASSWORD, admin.hashed_password):
            admin.hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
            db.commit()
    finally:
        db.close()
