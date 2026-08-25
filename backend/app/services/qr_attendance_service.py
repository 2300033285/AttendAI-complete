from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.qr_attendance import QRAttendance
from app.models.qr_code import QRCode
from app.models.employee import Employee
from app.models.user import User
from app.models.attendance import Attendance


# ==========================================
# SCAN QR AND MARK ATTENDANCE
# ==========================================

def scan_qr_attendance_service(
    db: Session,
    employee_id: int,
    qr_token: str
):

    # ==========================================
    # 1. CHECK QR TOKEN
    # ==========================================

    qr_code = (
        db.query(QRCode)
        .filter(
            QRCode.token == qr_token,
            QRCode.is_active == True
        )
        .first()
    )

    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or inactive QR code."
        )

    # ==========================================
    # 2. FIND EMPLOYEE
    # ==========================================

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )

    # ==========================================
    # 3. FIND USER USING EMPLOYEE EMAIL
    # ==========================================

    user = (
        db.query(User)
        .filter(User.email == employee.email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User account not found for this employee."
        )

    # ==========================================
    # 4. CURRENT DATE AND TIME
    # ==========================================

    now = datetime.now()
    today = now.date()
    current_time = now.time()

    # ==========================================
    # 5. CHECK TODAY'S ATTENDANCE
    # ==========================================

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user.id,
            Attendance.date == today
        )
        .order_by(Attendance.id.desc())
        .first()
    )

    # ==========================================
    # 6. FIRST SCAN → CHECK-IN
    # ==========================================

    if attendance is None:

        attendance = Attendance(
            user_id=user.id,
            date=today,
            check_in=current_time,
            check_out=None,
            status="Present"
        )

        db.add(attendance)
        db.flush()

        action = "Check-in"

    # ==========================================
    # 7. SECOND SCAN → CHECK-OUT
    # ==========================================

    elif attendance.check_out is None:

        attendance.check_out = current_time
        attendance.status = "Present"

        db.flush()

        action = "Check-out"

    # ==========================================
    # 8. ALREADY COMPLETED
    # ==========================================

    else:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already completed for today."
        )

    # ==========================================
    # 9. SAVE QR SCAN LOG
    # ==========================================

    qr_attendance = QRAttendance(
        employee_id=employee_id,
        qr_token=qr_token,
        status="Present"
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
        "message": f"{action} successful.",
        "employee_id": employee_id,
        "user_id": user.id,
        "attendance_id": attendance.id,
        "date": attendance.date,
        "check_in": attendance.check_in,
        "check_out": attendance.check_out,
        "status": attendance.status,
        "qr_attendance_id": qr_attendance.id
    }