from typing import List
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user

from app.models.user import User
from app.models.employee import Employee

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceHistoryResponse,
    AttendanceReportResponse,
)

from app.services.attendance_service import (
    create_attendance_service,
    get_all_attendance_service,
    get_attendance_service,
    update_attendance_service,
    delete_attendance_service,
    get_attendance_history_service,
    get_attendance_report_service,
)


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# =========================
# DIRECT CHECK-IN
# Disabled
# Attendance must be through QR scan
# =========================

@router.post(
    "/check-in",
    response_model=AttendanceResponse,
)
def check_in_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Check-in is only allowed by scanning an active QR code.",
    )


# =========================
# DIRECT CHECK-OUT
# Disabled
# Attendance must be through QR flow
# =========================

@router.post(
    "/check-out",
    response_model=AttendanceResponse,
)
def check_out_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Check-out is only allowed through the QR attendance flow.",
    )


# =========================
# CREATE ATTENDANCE
# =========================

@router.post(
    "/",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_attendance_api(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_attendance_service(
        db,
        attendance,
    )


# =========================
# ATTENDANCE HISTORY
# =========================

@router.get(
    "/history",
    response_model=List[AttendanceHistoryResponse],
)
def get_attendance_history(
    employee_id: int | None = Query(
        default=None,
        description="Employee ID - Admin only",
    ),
    start_date: date | None = Query(
        default=None,
        description="Start date (YYYY-MM-DD)",
    ),
    end_date: date | None = Query(
        default=None,
        description="End date (YYYY-MM-DD)",
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user.get("role")
    current_user_id = current_user.get("id")

    # Validate date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date.",
        )

    # =========================
    # ADMIN
    # =========================

    if role == "Admin":
        return get_attendance_history_service(
            db=db,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
        )

    # =========================
    # EMPLOYEE
    # =========================

    if role == "Employee":
        return get_attendance_history_service(
            db=db,
            user_id=current_user_id,
            start_date=start_date,
            end_date=end_date,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied.",
    )


# =========================
# ATTENDANCE REPORT
# =========================

@router.get(
    "/report",
    response_model=AttendanceReportResponse,
)
def get_attendance_report(
    start_date: date = Query(
        ...,
        description="Start date (YYYY-MM-DD)",
    ),
    end_date: date = Query(
        ...,
        description="End date (YYYY-MM-DD)",
    ),
    employee_id: int | None = Query(
        default=None,
        description="Employee ID - Admin only",
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user.get("role")
    current_user_id = current_user.get("id")

    # =========================
    # VALIDATE DATE RANGE
    # =========================

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be greater than end_date.",
        )

    # =========================
    # ADMIN REPORT
    # =========================

    if role == "Admin":

        if employee_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="employee_id is required for Admin reports.",
            )

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

        user = (
            db.query(User)
            .filter(User.email == employee.email)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found for employee.",
            )

        return get_attendance_report_service(
            db=db,
            user_id=user.id,
            employee_id=employee.id,
            start_date=start_date,
            end_date=end_date,
        )

    # =========================
    # EMPLOYEE REPORT
    # =========================

    if role == "Employee":

        employee = (
            db.query(Employee)
            .filter(
                Employee.email == current_user.get("sub")
            )
            .first()
        )

        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found.",
            )

        return get_attendance_report_service(
            db=db,
            user_id=current_user_id,
            employee_id=employee.id,
            start_date=start_date,
            end_date=end_date,
        )

    # =========================
    # INVALID ROLE
    # =========================

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied.",
    )


# =========================
# GET ALL ATTENDANCE
# =========================

@router.get(
    "/",
    response_model=List[AttendanceResponse],
)
def get_attendance_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_attendance_service(db)


# =========================
# GET ATTENDANCE BY ID
# =========================

@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def get_attendance_by_id_api(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attendance = get_attendance_service(
        db,
        attendance_id,
    )

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found",
        )

    return attendance


# =========================
# UPDATE ATTENDANCE
# =========================

@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse,
)
def update_attendance_api(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated = update_attendance_service(
        db,
        attendance_id,
        attendance,
    )

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found",
        )

    return updated


# =========================
# DELETE ATTENDANCE
# =========================

@router.delete(
    "/{attendance_id}",
)
def delete_attendance_api(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = delete_attendance_service(
        db,
        attendance_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance not found",
        )

    return {
        "message": "Attendance deleted successfully"
    }