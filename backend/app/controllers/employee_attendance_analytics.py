from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee_attendance_analytics import (
    EmployeeAttendanceAnalyticsResponse
)
from app.services.employee_attendance_analytics_service import (
    employee_attendance_analytics_service
)


router = APIRouter(
    prefix="/employee-attendance-analytics",
    tags=["Employee Attendance Analytics"]
)


@router.get(
    "/",
    response_model=List[EmployeeAttendanceAnalyticsResponse]
)
def get_employee_attendance_analytics(
    db: Session = Depends(get_db)
):
    return employee_attendance_analytics_service(db)