from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.qr_attendance import QRAttendance
from app.models.qr_code import QRCode
from app.models.employee import Employee
from app.models.user import User
from app.models.attendance import Attendance

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
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )

    # ==========================================
    # 4. FIND USER USING EMPLOYEE EMAIL
    # ==========================================

    user = (
        db.query(User)
        .filter(User.email == employee.email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found for this employee.",
        )

    # ==========================================
    # 5. FIND TODAY'S ATTENDANCE
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
    # 6. FIRST SCAN → CHECK-IN
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
    # 7. SECOND SCAN → CHECK-OUT
    # ==========================================

    elif attendance.check_in is not None and attendance.check_out is None:

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
    # 8. ALREADY CHECKED OUT
    # ==========================================

    else:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee has already checked out today.",
        )

    # ==========================================
    # 9. SAVE QR SCAN LOG
    # ==========================================

    qr_attendance = QRAttendance(
        employee_id=employee_id,
        qr_token=qr_token,
        status=qr_status,
    )

    db.add(qr_attendance)

    # ==========================================
    # 10. COMMIT
    # ==========================================

    db.commit()

    db.refresh(attendance)
    db.refresh(qr_attendance)

    # ==========================================
    # 11. RETURN RESULT
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
