from datetime import time

from sqlalchemy import func, case, and_
from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def get_analytics(db: Session):

    # =====================================================
    # ATTENDANCE CONDITIONS
    # =====================================================

    present_condition = (
        func.lower(Attendance.status) == "present"
    )

    absent_condition = (
        func.lower(Attendance.status) == "absent"
    )

    late_status_condition = (
        func.lower(Attendance.status) == "late"
    )

    # Present records with valid check-in and check-out
    working_condition = and_(
        present_condition,
        Attendance.check_in.isnot(None),
        Attendance.check_out.isnot(None)
    )

    # Late records:
    # 1. Explicitly marked as Late
    # 2. Present but checked in after 09:00
    late_condition = and_(
        Attendance.check_in.isnot(None),
        (
            late_status_condition
            | and_(
                present_condition,
                Attendance.check_in > time(9, 0)
            )
        )
    )

    # =====================================================
    # DATABASE AGGREGATION
    # =====================================================

    result = db.query(
        func.count(Attendance.id).label(
            "total_records"
        ),

        func.sum(
            case(
                (present_condition, 1),
                else_=0
            )
        ).label("present_days"),

        func.sum(
            case(
                (absent_condition, 1),
                else_=0
            )
        ).label("absent_days"),

        func.sum(
            case(
                (late_condition, 1),
                else_=0
            )
        ).label("late_count"),

        func.avg(
            case(
                (
                    working_condition,
                    func.extract(
                        "epoch",
                        Attendance.check_out
                        - Attendance.check_in
                    ) / 3600.0
                ),
                else_=None
            )
        ).label("average_hours")

    ).one()

    # =====================================================
    # HANDLE NULL VALUES
    # =====================================================

    total_records = result.total_records or 0
    present_days = result.present_days or 0
    absent_days = result.absent_days or 0
    late_count = result.late_count or 0
    average_hours = result.average_hours or 0

    # =====================================================
    # ATTENDANCE PERCENTAGE
    # =====================================================

    attendance_percentage = (
        (present_days / total_records) * 100
        if total_records > 0
        else 0
    )

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {
        "attendance_percentage": round(
            attendance_percentage,
            2
        ),
        "present_days": int(present_days),
        "absent_days": int(absent_days),
        "late_count": int(late_count),
        "average_hours": round(
            float(average_hours),
            2
        )
    }