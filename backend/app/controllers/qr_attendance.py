from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.qr_attendance import (
    QRAttendanceScan,
    QRAttendanceResponse
)
from app.services.qr_attendance_service import (
    scan_qr_attendance_service
)
from app.security import get_current_user
from app.models.employee import Employee


router = APIRouter(
    prefix="/qr-attendance",
    tags=["QR Attendance"]
)


@router.post(
    "/scan",
    response_model=QRAttendanceResponse,
    status_code=status.HTTP_201_CREATED
)
def scan_qr_attendance(
    qr_data: QRAttendanceScan,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    print("CURRENT USER:", current_user)

    # Get email from JWT token
    user_email = current_user.get("sub")

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User email missing from authentication token"
        )

    # Find employee using the same email
    employee = (
        db.query(Employee)
        .filter(Employee.email == user_email)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employee profile found for this user"
        )

    print("USER EMAIL:", user_email)
    print("EMPLOYEE ID:", employee.id)

    return scan_qr_attendance_service(
        db=db,
        employee_id=employee.id,
        qr_token=qr_data.qr_token
    )