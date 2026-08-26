from sqlalchemy.orm import Session

from app.crud.employee_attendance_analytics import (
    get_employee_attendance_analytics
)


def employee_attendance_analytics_service(
    db: Session
):

    return get_employee_attendance_analytics(db)