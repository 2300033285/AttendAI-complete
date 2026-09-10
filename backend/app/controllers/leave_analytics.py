from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles
from app.services.leave_analytics_service import (
    get_leave_summary_service,
    get_leave_type_summary_service,
    get_employee_leave_summary_service,
    get_monthly_leave_summary_service,
    get_leave_days_summary_service,
)

router = APIRouter(
    prefix="/leave-analytics",
    tags=["Leave Analytics"],
    dependencies=[Depends(require_roles(["Admin"]))]
)


@router.get("/summary")
def leave_summary(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_leave_summary_service(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )


@router.get("/by-type")
def leave_by_type(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_leave_type_summary_service(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )


@router.get("/by-employee")
def leave_by_employee(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_employee_leave_summary_service(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )
@router.get("/monthly")
def leave_monthly(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_monthly_leave_summary_service(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )
@router.get("/days")
def leave_days(
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return get_leave_days_summary_service(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )