from datetime import date, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.qr_attendance import QRAttendance
from app.models.qr_code import QRCode
from app.models.employee import Employee
from app.models.user import User
from app.models.attendance import Attendance
from app.models.shift import Shift

from app.services.attendance_service import (
    check_in_service,
    check_out_service,
)


# ==========================================
# SCAN QR AND MARK CHECK-IN / CHECK-OUT
# ==========================================

def scan_qr_attendance_service(
    db: Session,
    employee_id: int,
    qr_token: str,
):

    # ==========================================
    # 1. CHECK QR TOKEN
    # ==========================================

    qr_code = (
        db.query(QRCode)
        .filter(
            QRCode.token == qr_token,
            QRCode.is_active == True,
        )
        .first()
    )

    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or inactive QR code.",
        )

    # ==========================================
    # 2. CHECK QR ASSIGNMENT
    # ==========================================

    if qr_code.employee_id != employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This QR code is not assigned to this employee.",
        )

    # ==========================================
    # 3. FIND EMPLOYEE
    # ==========================================

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    # ==========================================
    # 4. FIND USER
    # ==========================================

    user = (
        db.query(User)
        .filter(
            User.email == employee.email
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found for this employee.",
        )

    # ==========================================
    # 5. FIND EMPLOYEE SHIFT
    # ==========================================

    shift = (
        db.query(Shift)
        .filter(
            Shift.id == employee.shift_id
        )
        .first()
    )

    if shift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not assigned to this employee.",
        )

    # ==========================================
    # 6. FIND TODAY'S ATTENDANCE
    # ==========================================

    today = date.today()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user.id,
            Attendance.date == today,
        )
        .first()
    )

    # ==========================================
    # 7. FIRST QR SCAN → CHECK-IN
    # ==========================================

    if attendance is None:

        attendance, error = check_in_service(
            db,
            user.id,
        )

        if error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error,
            )

        qr_status = "Check-in"
        message = "Check-in successful."

    # ==========================================
    # 8. SECOND QR SCAN → CHECK-OUT
    # ==========================================

    elif (
        attendance.check_in is not None
        and attendance.check_out is None
    ):

        current_time = datetime.now()

        # ------------------------------------------
        # Scheduled shift start and end
        # ------------------------------------------

        shift_start = datetime.combine(
            today,
            shift.start_time,
        )

        shift_end = datetime.combine(
            today,
            shift.end_time,
        )

        # ------------------------------------------
        # Employee actual check-in time
        # ------------------------------------------

        check_in_datetime = datetime.combine(
            today,
            attendance.check_in,
        )

        # ------------------------------------------
        # Calculate late minutes
        # ------------------------------------------

        late_minutes = 0

        if check_in_datetime > shift_start:

            late_minutes = int(
                (
                    check_in_datetime - shift_start
                ).total_seconds() / 60
            )

        # ------------------------------------------
        # Calculate required checkout time
        # ------------------------------------------

        if late_minutes >= 30:

            # Employee was 30 minutes or more late.
            # Add the complete late duration
            # to the normal shift end time.

            required_checkout = (
                shift_end
                + timedelta(minutes=late_minutes)
            )

        else:

            # Less than 30 minutes late.
            # Normal shift end time applies.

            required_checkout = shift_end

        # ------------------------------------------
        # Prevent early checkout
        # ------------------------------------------

        if current_time < required_checkout:

            remaining_seconds = int(
                (
                    required_checkout - current_time
                ).total_seconds()
            )

            remaining_minutes = (
                remaining_seconds // 60
            )

            remaining_seconds = (
                remaining_seconds % 60
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot check out yet. "
                    f"Required checkout time is "
                    f"{required_checkout.strftime('%H:%M:%S')}. "
                    f"Remaining time: "
                    f"{remaining_minutes} minutes "
                    f"{remaining_seconds} seconds."
                ),
            )

        # ------------------------------------------
        # Checkout allowed
        # ------------------------------------------

        attendance, error = check_out_service(
            db,
            user.id,
        )

        if error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error,
            )

        qr_status = "Check-out"
        message = "Check-out successful."

    # ==========================================
    # 9. ALREADY CHECKED OUT
    # ==========================================

    else:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee has already checked out today.",
        )

    # ==========================================
    # 10. SAVE QR SCAN LOG
    # ==========================================

    qr_attendance = QRAttendance(
        employee_id=employee_id,
        qr_token=qr_token,
        status=qr_status,
    )

    db.add(qr_attendance)

    # ==========================================
    # 11. COMMIT
    # ==========================================

    db.commit()

    db.refresh(attendance)
    db.refresh(qr_attendance)

    # ==========================================
    # 12. RETURN RESULT
    # ==========================================

    return {
        "message": message,
        "employee_id": employee_id,
        "user_id": user.id,
        "attendance_id": attendance.id,
        "date": attendance.date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status,
        "qr_attendance_id": qr_attendance.id,
    }