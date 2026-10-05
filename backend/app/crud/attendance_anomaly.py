from sqlalchemy.orm import Session

from app.models.attendance import Attendance


def get_anomalies(db: Session):

    attendance_records = (
        db.query(Attendance)
        .order_by(Attendance.date, Attendance.id)
        .all()
    )

    anomalies = []

    for record in attendance_records:

        status = (record.status or "").strip().lower()

        # =====================================================
        # 1. ABSENT ATTENDANCE
        # =====================================================

        if status == "absent":

            anomalies.append({
                "attendance_id": record.id,
                "user_id": record.user_id,
                "status": "Absent"
            })

            continue

        # =====================================================
        # 2. LATE ATTENDANCE
        # =====================================================

        if status == "late":

            anomalies.append({
                "attendance_id": record.id,
                "user_id": record.user_id,
                "status": "Late"
            })

        # =====================================================
        # 3. INCOMPLETE ATTENDANCE
        # =====================================================

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
                "status": "Incomplete Attendance"
            })

            continue

        # =====================================================
        # 4. EXCESSIVE WORKING HOURS
        # =====================================================

        if (
            status in ["present", "late"]
            and record.check_in
            and record.check_out
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

            worked_minutes = end_minutes - start_minutes
            worked_hours = worked_minutes / 60

            # More than 10 hours
            if worked_hours > 10:

                anomalies.append({
                    "attendance_id": record.id,
                    "user_id": record.user_id,
                    "status": "Excessive Working Hours"
                })

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }