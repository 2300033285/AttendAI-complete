from sqlalchemy.orm import Session

from app.crud.leave_reports import (
    get_leave_report_summary,
    get_leave_report_by_employee,
    get_leave_report_by_type,
    get_monthly_leave_report,
)


def get_leave_report_summary_service(
    db: Session,
    employee_id: int | None = None,
):
    return get_leave_report_summary(
        db=db,
        employee_id=employee_id,
    )


def get_leave_report_by_employee_service(
    db: Session,
):
    return get_leave_report_by_employee(
        db=db,
    )


def get_leave_report_by_type_service(
    db: Session,
):
    return get_leave_report_by_type(
        db=db,
    )


def get_monthly_leave_report_service(
    db: Session,
    year: int | None = None,
):
    return get_monthly_leave_report(
        db=db,
        year=year,
    )