from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.qr_attendance import QRAttendance


# ==========================================
# SCAN QR AND MARK ATTENDANCE
# ==========================================

def scan_qr_attendance_service(
    db: Session,
    employee_id: int,
    qr_token: str
):

    # Check whether this employee has already used this QR token
    attendance = (
        db.query(QRAttendance)
        .filter(
            QRAttendance.employee_id == employee_id,
            QRAttendance.qr_token == qr_token
        )
        .first()
    )

    if attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance has already been marked for this QR code."
        )

    # Create attendance record
    new_attendance = QRAttendance(
        employee_id=employee_id,
        qr_token=qr_token,
        status="Present"
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance