
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.attendance import Attendance


def get_attendance_ai_features(
    db: Session,
    user_id: int,
):
    records = (
        db.query(Attendance)
        .filter(Attendance.user_id == user_id)
        .order_by(Attendance.date.asc())
        .all()
    )

    if not records:
        return {
            "user_id": user_id,
            "total_records": 0,
            "present_count": 0,
            "late_count": 0,
            "absent_count": 0,
            "attendance_percentage": 0.0,
            "late_percentage": 0.0,
            "absence_percentage": 0.0,
            "average_working_hours": 0.0,
        }

    total = len(records)

    present_count = sum(
        1 for r in records
        if (r.status or "").strip().lower() == "present"
    )

    late_count = sum(
        1 for r in records
        if (r.status or "").strip().lower() == "late"
    )

    absent_count = sum(
        1 for r in records
        if (r.status or "").strip().lower() == "absent"
    )

    attendance_percentage = round(
        (present_count + late_count) / total * 100, 2
    )

    late_percentage = round(late_count / total * 100, 2)

    absence_percentage = round(absent_count / total * 100, 2)

    working_hours = []

    for record in records:
        if record.check_in and record.check_out:
            start = (
                record.check_in.hour * 60
                + record.check_in.minute
            )

            end = (
                record.check_out.hour * 60
                + record.check_out.minute
            )

            # Handle overnight attendance.
            if end <= start:
                end += 24 * 60

            working_hours.append((end - start) / 60)

    average_working_hours = (
        round(sum(working_hours) / len(working_hours), 2)
        if working_hours
        else 0.0
    )

    return {
        "user_id": user_id,
        "total_records": total,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "attendance_percentage": attendance_percentage,
        "late_percentage": late_percentage,
        "absence_percentage": absence_percentage,
        "average_working_hours": average_working_hours,
    }
