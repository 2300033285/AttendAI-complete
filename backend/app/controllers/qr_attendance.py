from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.security import get_current_user

from app.models.qr_code import QRCode
from app.models.employee import Employee

from app.schemas.qr_attendance import (
    QRAttendanceScan,
    QRAttendanceResponse,
)

from app.services.qr_attendance_service import (
    scan_qr_attendance_service,
)

from app.crud.qr_analytics import (
    get_qr_analytics,
    get_daily_qr_analytics,
    get_employee_qr_analytics,
)

from app.crud.qr_anomaly import get_qr_anomalies

from app.schemas.qr_analytics import (
    QRDailyAnalyticsResponse,
    QREmployeeAnalyticsResponse,
)

from app.schemas.qr_anomaly import QRAnomalyResponse


router = APIRouter(
    prefix="/qr-attendance",
    tags=["QR Attendance"],
)


# =========================================================
# SCAN QR ATTENDANCE
# Employee scans the QR code
# =========================================================

@router.post(
    "/scan",
    response_model=QRAttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def scan_qr_attendance(
    qr_data: QRAttendanceScan,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    print("CURRENT USER:", current_user)

    # -----------------------------------------------------
    # Get email from JWT token
    # -----------------------------------------------------

    user_email = current_user.get("sub")

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User email missing from authentication token",
        )

    # -----------------------------------------------------
    # Find employee using email
    # -----------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(Employee.email == user_email)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employee profile found for this user",
        )

    print("USER EMAIL:", user_email)
    print("EMPLOYEE ID:", employee.id)

    # -----------------------------------------------------
    # Process QR attendance
    # -----------------------------------------------------

    return scan_qr_attendance_service(
        db=db,
        employee_id=employee.id,
        qr_token=qr_data.qr_token,
    )


# =========================================================
# GENERATE QR TOKEN
# ADMIN ONLY
# QR IS ASSIGNED TO AN EMPLOYEE
# =========================================================

@router.post("/generate")
def generate_qr_token(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # -----------------------------------------------------
    # Check Admin role
    # -----------------------------------------------------

    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    # -----------------------------------------------------
    # Check employee exists
    # -----------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    # -----------------------------------------------------
    # Generate unique QR token
    # -----------------------------------------------------

    token = str(uuid.uuid4())

    # -----------------------------------------------------
    # Save QR token assigned to employee
    # -----------------------------------------------------

    qr_code = QRCode(
        token=token,
        employee_id=employee_id,
        is_active=True,
    )

    db.add(qr_code)
    db.commit()
    db.refresh(qr_code)

    # -----------------------------------------------------
    # Return QR information
    # -----------------------------------------------------

    return {
        "message": "QR token generated successfully",
        "qr_code_id": qr_code.id,
        "employee_id": qr_code.employee_id,
        "qr_token": qr_code.token,
        "is_active": qr_code.is_active,
    }


# =========================================================
# QR ATTENDANCE ANALYTICS
# ADMIN ONLY
# =========================================================

@router.get("/analytics")
def qr_attendance_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return get_qr_analytics(db)


# =========================================================
# DAILY QR ANALYTICS
# ADMIN ONLY
# =========================================================

@router.get(
    "/analytics/daily",
    response_model=list[QRDailyAnalyticsResponse],
)
def qr_attendance_daily_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return get_daily_qr_analytics(db)


# =========================================================
# EMPLOYEE QR ANALYTICS
# ADMIN ONLY
# =========================================================

@router.get(
    "/analytics/employee",
    response_model=list[QREmployeeAnalyticsResponse],
)
def qr_attendance_employee_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return get_employee_qr_analytics(db)


# =========================================================
# QR ATTENDANCE ANOMALIES
# ADMIN ONLY
# =========================================================

@router.get(
    "/analytics/anomalies",
    response_model=list[QRAnomalyResponse],
)
def qr_attendance_anomalies(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return get_qr_anomalies(db)