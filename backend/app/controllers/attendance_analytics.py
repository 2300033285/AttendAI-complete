from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.attendance_analytics_service import attendance_analytics_service
from app.schemas.attendance_analytics import AttendanceAnalyticsResponse


router = APIRouter(
    prefix="/attendance-analytics",
    tags=["Attendance Analytics"]
)


@router.get(
    "/",
    response_model=AttendanceAnalyticsResponse
)
def get_attendance_analytics(
    db: Session = Depends(get_db)
):
    return attendance_analytics_service(db)