from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
)

from app.services.attendance_service import (
    create_attendance_service,
    get_all_attendance_service,
    get_attendance_service,
    update_attendance_service,
    delete_attendance_service,
    check_in_service,
    check_out_service,
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


# =========================
# CHECK-IN
# =========================

@router.post(
    "/check-in",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def check_in_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attendance, error = check_in_service(
        db,
        current_user["id"],
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return attendance


# =========================
# CHECK-OUT
# =========================

@router.post(
    "/check-out",
    response_model=AttendanceResponse,
)
def check_out_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    attendance, error = check_out_service(
        db,
        current_user["id"],
    )

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    return attendance


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
    return create_attendance_service(db, attendance)


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