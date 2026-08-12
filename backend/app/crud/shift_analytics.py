from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.models.attendance import Attendance


def get_shift_analytics(db: Session):

    # Get all shifts
    shifts = db.query(Shift).all()

    # Get all attendance records
    attendance_records = db.query(Attendance).all()

    # If there are no shifts
    if not shifts:
        return {
            "total_shifts": 0,
            "completed_shifts": 0,
            "missed_shifts": 0,
            "average_shift_hours": 0,
            "overtime_hours": 0,
            "shift_wise_attendance": {}
        }

    # -------------------------------------------------
    # 1. TOTAL SHIFTS
    # -------------------------------------------------

    total_shifts = len(shifts)

    # -------------------------------------------------
    # 2. COMPLETED AND MISSED SHIFTS
    # -------------------------------------------------

    completed_shifts = 0
    missed_shifts = 0

    for attendance in attendance_records:

        if (
            attendance.status
            and attendance.status.lower() == "present"
        ):
            completed_shifts += 1

        elif (
            attendance.status
            and attendance.status.lower() == "absent"
        ):
            missed_shifts += 1

    # -------------------------------------------------
    # 3. AVERAGE SHIFT HOURS
    # -------------------------------------------------

    total_shift_minutes = 0
    valid_shift_count = 0

    for shift in shifts:

        if shift.start_time and shift.end_time:

            start_minutes = (
                shift.start_time.hour * 60
                + shift.start_time.minute
            )

            end_minutes = (
                shift.end_time.hour * 60
                + shift.end_time.minute
            )

            # Handle overnight shifts
            if end_minutes <= start_minutes:
                end_minutes += 24 * 60

            duration = end_minutes - start_minutes

            total_shift_minutes += duration
            valid_shift_count += 1

    if valid_shift_count > 0:

        average_shift_hours = round(
            total_shift_minutes / valid_shift_count / 60,
            2
        )

    else:
        average_shift_hours = 0

    # -------------------------------------------------
    # 4. OVERTIME
    # -------------------------------------------------

    total_overtime_minutes = 0

    for attendance in attendance_records:

        # Only calculate overtime for Present records
        if (
            attendance.status
            and attendance.status.lower() == "present"
            and attendance.check_in
            and attendance.check_out
        ):

            start_minutes = (
                attendance.check_in.hour * 60
                + attendance.check_in.minute
            )

            end_minutes = (
                attendance.check_out.hour * 60
                + attendance.check_out.minute
            )

            # Handle overnight attendance
            if end_minutes <= start_minutes:
                end_minutes += 24 * 60

            worked_minutes = end_minutes - start_minutes

            # Standard working time = 8 hours
            standard_minutes = 8 * 60

            if worked_minutes > standard_minutes:

                total_overtime_minutes += (
                    worked_minutes - standard_minutes
                )

    overtime_hours = round(
        total_overtime_minutes / 60,
        2
    )

    # -------------------------------------------------
    # 5. SHIFT-WISE ATTENDANCE
    # -------------------------------------------------

    shift_wise_attendance = {}

    for shift in shifts:

        shift_name = shift.shift_name

        present_count = 0
        absent_count = 0

        for attendance in attendance_records:

            # If there is no check-in, we cannot determine
            # which shift the absent record belongs to.
            # Therefore, do NOT count it for every shift.
            if not attendance.check_in:
                continue

            check_in_minutes = (
                attendance.check_in.hour * 60
                + attendance.check_in.minute
            )

            shift_start_minutes = (
                shift.start_time.hour * 60
                + shift.start_time.minute
            )

            shift_end_minutes = (
                shift.end_time.hour * 60
                + shift.end_time.minute
            )

            # Normal shift
            if shift_end_minutes > shift_start_minutes:

                is_matching_shift = (
                    shift_start_minutes
                    <= check_in_minutes
                    < shift_end_minutes
                )

            # Overnight shift
            else:

                is_matching_shift = (
                    check_in_minutes >= shift_start_minutes
                    or check_in_minutes < shift_end_minutes
                )

            if is_matching_shift:

                if (
                    attendance.status
                    and attendance.status.lower() == "present"
                ):
                    present_count += 1

                elif (
                    attendance.status
                    and attendance.status.lower() == "absent"
                ):
                    absent_count += 1

        shift_wise_attendance[shift_name] = {
            "present": present_count,
            "absent": absent_count,
            "total": present_count + absent_count
        }

    # -------------------------------------------------
    # FINAL RESPONSE
    # -------------------------------------------------

    return {
        "total_shifts": total_shifts,
        "completed_shifts": completed_shifts,
        "missed_shifts": missed_shifts,
        "average_shift_hours": average_shift_hours,
        "overtime_hours": overtime_hours,
        "shift_wise_attendance": shift_wise_attendance
    }