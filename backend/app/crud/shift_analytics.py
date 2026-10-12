
from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.models.attendance import Attendance


def get_shift_analytics(db: Session):
    shifts = db.query(Shift).all()
    attendance_records = db.query(Attendance).all()

    # Count attendance records by status.
    completed_shifts = sum(
        1
        for record in attendance_records
        if (record.status or "").strip().lower() in ("present", "late")
    )

    missed_shifts = sum(
        1
        for record in attendance_records
        if (record.status or "").strip().lower() == "absent"
    )

    # Return zero shift metrics if no shifts are configured.
    if not shifts:
        total_overtime_minutes = 0

        for record in attendance_records:
            status = (record.status or "").strip().lower()

            if (
                status in ("present", "late")
                and record.check_in is not None
                and record.check_out is not None
            ):
                start = (
                    record.check_in.hour * 60
                    + record.check_in.minute
                )
                end = (
                    record.check_out.hour * 60
                    + record.check_out.minute
                )

                if end <= start:
                    end += 24 * 60

                total_overtime_minutes += max(0, end - start - 480)

        return {
            "total_shifts": 0,
            "completed_shifts": completed_shifts,
            "missed_shifts": missed_shifts,
            "average_shift_hours": 0,
            "overtime_hours": round(total_overtime_minutes / 60, 2),
            "shift_wise_attendance": {},
        }

    # Calculate average duration of configured shifts.
    total_shift_minutes = 0
    valid_shift_count = 0

    for shift in shifts:
        if shift.start_time is None or shift.end_time is None:
            continue

        start = (
            shift.start_time.hour * 60
            + shift.start_time.minute
        )
        end = (
            shift.end_time.hour * 60
            + shift.end_time.minute
        )

        if end <= start:
            end += 24 * 60

        total_shift_minutes += end - start
        valid_shift_count += 1

    average_shift_hours = (
        round(total_shift_minutes / valid_shift_count / 60, 2)
        if valid_shift_count
        else 0
    )

    # Calculate overtime beyond 8 hours per attendance record.
    total_overtime_minutes = 0

    for record in attendance_records:
        status = (record.status or "").strip().lower()

        if (
            status in ("present", "late")
            and record.check_in is not None
            and record.check_out is not None
        ):
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

            worked_minutes = end - start
            total_overtime_minutes += max(0, worked_minutes - 480)

    overtime_hours = round(total_overtime_minutes / 60, 2)

    # Estimate shift-wise attendance using check-in time.
    # Exact assignment requires a shift_id in the Attendance model.
    shift_wise_attendance = {}

    for shift in shifts:
        present_count = 0
        absent_count = 0

        if shift.start_time is None or shift.end_time is None:
            shift_wise_attendance[shift.shift_name] = {
                "present": 0,
                "absent": 0,
                "total": 0,
            }
            continue

        start = (
            shift.start_time.hour * 60
            + shift.start_time.minute
        )
        end = (
            shift.end_time.hour * 60
            + shift.end_time.minute
        )

        for record in attendance_records:
            if record.check_in is None:
                continue

            check_in = (
                record.check_in.hour * 60
                + record.check_in.minute
            )

            # Match normal and overnight shifts.
            if end > start:
                matches = start <= check_in < end
            else:
                matches = check_in >= start or check_in < end

            if not matches:
                continue

            status = (record.status or "").strip().lower()

            if status in ("present", "late"):
                present_count += 1
            elif status == "absent":
                absent_count += 1

        shift_wise_attendance[shift.shift_name] = {
            "present": present_count,
            "absent": absent_count,
            "total": present_count + absent_count,
        }

    return {
        "total_shifts": len(shifts),
        "completed_shifts": completed_shifts,
        "missed_shifts": missed_shifts,
        "average_shift_hours": average_shift_hours,
        "overtime_hours": overtime_hours,
        "shift_wise_attendance": shift_wise_attendance,
    }
