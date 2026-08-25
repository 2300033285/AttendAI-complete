from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user

from app.crud.qr_analytics import (
    get_qr_analytics,
    get_daily_qr_analytics,
    get_employee_qr_analytics,
)

router = APIRouter(
    prefix="/qr-analytics",
    tags=["QR Analytics"],
)


@router.get("/")
def qr_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_qr_analytics(db)


@router.get("/daily")
def daily_qr_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = get_daily_qr_analytics(db)

    return [
        {
            "date": str(row.scan_date),
            "total_scans": row.total_scans,
            "present_scans": row.present_scans,
            "other_status_scans": row.other_status_scans,
        }
        for row in data
    ]


@router.get("/employee")
def employee_qr_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = get_employee_qr_analytics(db)

    return [
        {
            "employee_id": row.employee_id,
            "total_scans": row.total_scans,
            "present_scans": row.present_scans,
            "other_status_scans": row.other_status_scans,
        }
        for row in data
    ]