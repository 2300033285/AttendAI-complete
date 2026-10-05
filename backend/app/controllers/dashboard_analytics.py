from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.dashboard_analytics_service import (
    get_dashboard_analytics,
)

router = APIRouter(
    prefix="/dashboard-analytics",
    tags=["Dashboard Analytics"],
)


@router.get("/")
def dashboard_analytics(
    db: Session = Depends(get_db),
):
    return get_dashboard_analytics(db)