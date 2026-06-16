from app.config import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_USERNAME,
)
from app.database import Base, SessionLocal, engine
from app.models import Admin
from app.auth import get_password_hash


def init_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        admin = db.query(Admin).first()

        if admin:
            admin.username = DEFAULT_ADMIN_USERNAME
            admin.email = DEFAULT_ADMIN_EMAIL
            admin.hashed_password = get_password_hash(DEFAULT_ADMIN_PASSWORD)
        else:
            admin = Admin(
                username=DEFAULT_ADMIN_USERNAME,
                email=DEFAULT_ADMIN_EMAIL,
                hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
            )
            db.add(admin)

        db.commit()

    finally:
        db.close()