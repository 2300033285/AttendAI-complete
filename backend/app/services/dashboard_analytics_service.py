from sqlalchemy.orm import Session

from app.crud.analytics import get_analytics
from app.crud.employee_analytics import get_employee_analytics
from app.crud.employee_attendance_analytics import (
    get_employee_attendance_analytics
)
from app.crud.leave_analytics import get_leave_summary
from app.crud.shift_analytics import get_shift_analytics
from app.crud.referral_analytics import get_referral_analytics


def get_dashboard_analytics(db: Session):

    employee_analytics = get_employee_analytics(db)

    attendance_analytics = get_analytics(db)

    employee_attendance_analytics = (
        get_employee_attendance_analytics(db)
    )

    leave_analytics = get_leave_summary(db)

    shift_analytics = get_shift_analytics(db)

    referral_analytics = get_referral_analytics(db)

    return {
        "employee_analytics": employee_analytics,
        "attendance_analytics": attendance_analytics,
        "employee_attendance_analytics": employee_attendance_analytics,
        "leave_analytics": leave_analytics,
        "shift_analytics": shift_analytics,
        "referral_analytics": referral_analytics,
    }