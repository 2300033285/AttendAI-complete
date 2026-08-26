from sqlalchemy.orm import Session
from app.models.attendance import Attendance


def get_employee_attendance_analytics(db: Session):

    records = (
        db.query(Attendance)
        .order_by(Attendance.user_id, Attendance.date)
        .all()
    )

    employee_data = {}

    for record in records:

        employee_id = record.user_id

        if employee_id not in employee_data:
            employee_data[employee_id] = {
                "employee_id": employee_id,
                "total_records": 0,
                "present_days": 0,
                "absent_days": 0,
                "late_count": 0,
                "total_hours": 0,
                "working_records": 0,
            }

        data = employee_data[employee_id]

        data["total_records"] += 1

        status = (record.status or "").lower()

        if status == "present":
            data["present_days"] += 1

        elif status == "absent":
            data["absent_days"] += 1

        # Late after 9:00 AM
        if (
            record.check_in
            and record.check_in.hour > 9
        ) or (
            record.check_in
            and record.check_in.hour == 9
            and record.check_in.minute > 0
        ):
            data["late_count"] += 1

        # Calculate working hours
        if record.check_in and record.check_out:

            from datetime import datetime, timedelta

            start = datetime.combine(
                record.date,
                record.check_in
            )

            end = datetime.combine(
                record.date,
                record.check_out
            )

            # Handle overnight shifts
            if end < start:
                end += timedelta(days=1)

            hours = (
                end - start
            ).total_seconds() / 3600

            data["total_hours"] += hours
            data["working_records"] += 1

    results = []

    for employee_id, data in employee_data.items():

        total_records = data["total_records"]
        present_days = data["present_days"]

        attendance_percentage = (
            (present_days / total_records) * 100
            if total_records > 0
            else 0
        )

        average_hours = (
            data["total_hours"] / data["working_records"]
            if data["working_records"] > 0
            else 0
        )

        results.append({
            "employee_id": employee_id,
            "total_records": total_records,
            "present_days": present_days,
            "absent_days": data["absent_days"],
            "late_count": data["late_count"],
            "attendance_percentage": round(
                attendance_percentage,
                2
            ),
            "average_hours": round(
                average_hours,
                2
            ),
        })

    return results