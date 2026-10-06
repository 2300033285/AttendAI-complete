from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.models.attendance import Attendance


def get_shift_analytics(db: Session):
    shifts = db.query(Shift).all()
    attendance_records = db.query(Attendance).all()

    if not shifts:
        return {
            "total_shifts": 0,
            "completed_shifts": 0,
            "missed_shifts": 0,
            "average_shift_hours": 0,
            "overtime_hours": 0,
            "shift_wise_attendance": {},
        }

    # Count attendance records, not shift definitions.
    completed_shifts = sum(
        1 for record in attendance_records
        if (record.status or "").strip().lower() == "present"
    )

    missed_shifts = sum(
        1 for record in attendance_records
        if (record.status or "").strip().lower() == "absent"
    )

    # Calculate average duration of defined shifts.
    total_shift_minutes = 0
    valid_shift_count = 0

    for shift in shifts:
        if shift.start_time and shift.end_time:
            start = shift.start_time.hour * 60 + shift.start_time.minute
            end = shift.end_time.hour * 60 + shift.end_time.minute

            if end <= start:
                end += 24 * 60

            total_shift_minutes += end - start
            valid_shift_count += 1

    average_shift_hours = (
        round(total_shift_minutes / valid_shift_count / 60, 2)
        if valid_shift_count else 0
    )

    # Calculate overtime for present attendance records.
    total_overtime_minutes = 0

    for record in attendance_records:
        if (
            (record.status or "").strip().lower() == "present"
            and record.check_in
            and record.check_out
        ):
            start = record.check_in.hour * 60 + record.check_in.minute
            end = record.check_out.hour * 60 + record.check_out.minute

            if end <= start:
                end += 24 * 60

            worked_minutes = end - start
            total_overtime_minutes += max(0, worked_minutes - 480)

    overtime_hours = round(total_overtime_minutes / 60, 2)

    # Match records to shifts using check-in time.
    # Attendance has no shift_id, so this is an estimate.
    shift_wise_attendance = {}

    for shift in shifts:
        present_count = 0
        absent_count = 0

        if not shift.start_time or not shift.end_time:
            shift_wise_attendance[shift.shift_name] = {
                "present": 0,
                "absent": 0,
                "total": 0,
            }
            continue

        start = shift.start_time.hour * 60 + shift.start_time.minute
        end = shift.end_time.hour * 60 + shift.end_time.minute

        for record in attendance_records:
            if not record.check_in:
                continue

            check_in = record.check_in.hour * 60 + record.check_in.minute

            if end > start:
                matches = start <= check_in < end
            else:
                matches = check_in >= start or check_in < end

            if matches:
                status = (record.status or "").strip().lower()

                if status == "present":
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