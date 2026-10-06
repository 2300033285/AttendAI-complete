
from typing import Optional

from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def get_anomalies(
    db: Session,
    user_id: Optional[int] = None,
):
    query = db.query(Attendance)

    # Retrieve only one user's attendance when requested
    if user_id is not None:
        query = query.filter(Attendance.user_id == user_id)

    attendance_records = (
        query
        .order_by(Attendance.date, Attendance.id)
        .all()
    )

    anomalies = []

    for record in attendance_records:
        status = (record.status or "").strip().lower()

        # 1. Absent attendance
        if status == "absent":
            anomalies.append({
                "attendance_id": record.id,
                "user_id": record.user_id,
                "status": "Absent",
                "anomaly_type": "Absent Attendance",
                "severity": "Medium",
                "description": (
                    "Employee was marked absent for the attendance record."
                ),
                "source": "Rule-Based Detection",
            })
            continue

        # 2. Late attendance
        if status == "late":
            anomalies.append({
                "attendance_id": record.id,
                "user_id": record.user_id,
                "status": "Late",
                "anomaly_type": "Late Attendance",
                "severity": "Low",
                "description": (
                    "Employee was marked as late for the attendance record."
                ),
                "source": "Rule-Based Detection",
            })

        # 3. Incomplete attendance
        if (
            status in ["present", "late"]
            and (
                record.check_in is None
                or record.check_out is None
            )
        ):
            anomalies.append({
                "attendance_id": record.id,
                "user_id": record.user_id,
                "status": "Incomplete Attendance",
                "anomaly_type": "Incomplete Attendance",
                "severity": "Medium",
                "description": (
                    "Attendance record is missing check-in or check-out information."
                ),
                "source": "Rule-Based Detection",
            })
            continue

        # 4. Excessive working hours
        if (
            status in ["present", "late"]
            and record.check_in is not None
            and record.check_out is not None
        ):
            start_minutes = (
                record.check_in.hour * 60
                + record.check_in.minute
            )

            end_minutes = (
                record.check_out.hour * 60
                + record.check_out.minute
            )

            # Handle overnight attendance
            if end_minutes <= start_minutes:
                end_minutes += 24 * 60

            worked_hours = (end_minutes - start_minutes) / 60

            if worked_hours > 10:
                anomalies.append({
                    "attendance_id": record.id,
                    "user_id": record.user_id,
                    "status": "Excessive Working Hours",
                    "anomaly_type": "Excessive Working Hours",
                    "severity": "High",
                    "description": (
                        f"Employee worked for approximately "
                        f"{worked_hours:.2f} hours, exceeding "
                        "the 10-hour threshold."
                    ),
                    "source": "Rule-Based Detection",
                })

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies,
    }
