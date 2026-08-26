from sqlalchemy.orm import Session

from app.crud.analytics import get_analytics


def attendance_analytics_service(db: Session):
    return get_analytics(db)