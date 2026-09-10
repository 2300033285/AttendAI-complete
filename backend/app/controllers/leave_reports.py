from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.leave_reports_service import (
    get_leave_report_summary_service,
    get_leave_report_by_employee_service,
    get_leave_report_by_type_service,
    get_monthly_leave_report_service,
)


router = APIRouter(
    prefix="/leave-reports",
    tags=["Leave Reports"],
    dependencies=[
        Depends(require_roles(["Admin"]))
    ],
)


@router.get("/summary")
def leave_report_summary(
    employee_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_leave_report_summary_service(
        db=db,
        employee_id=employee_id,
    )


@router.get("/by-employee")
def leave_report_by_employee(
    db: Session = Depends(get_db),
):
    return get_leave_report_by_employee_service(
        db=db,
    )


@router.get("/by-type")
def leave_report_by_type(
    db: Session = Depends(get_db),
):
    return get_leave_report_by_type_service(
        db=db,
    )


@router.get("/monthly")
def monthly_leave_report(
    year: int | None = None,
    db: Session = Depends(get_db),
):
    return get_monthly_leave_report_service(
        db=db,
        year=year,
    )