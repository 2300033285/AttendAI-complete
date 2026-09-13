from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.crud.leave_analytics import (
    get_leave_summary,
    get_leave_type_summary,
    get_employee_leave_summary,
    get_monthly_leave_summary,
    get_leave_days_summary,
)


def get_leave_summary_service(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    return get_leave_summary(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )


def get_leave_type_summary_service(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
):
    results = get_leave_type_summary(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )

    return [
        {
            "leave_type": leave_type,
            "count": count,
        }
        for leave_type, count in results
    ]


def get_employee_leave_summary_service(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    results = get_employee_leave_summary(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )

    return [
        {
            "employee_id": employee_id,
            "leave_count": leave_count,
        }
        for employee_id, leave_count in results
    ]


def get_monthly_leave_summary_service(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    results = get_monthly_leave_summary(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )

    return [
        {
            "month": month,
            "leave_count": leave_count,
        }
        for month, leave_count in results
    ]


def get_leave_days_summary_service(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    results = get_leave_days_summary(
        db=db,
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        leave_type=leave_type,
        status=status,
    )

    return [
        {
            "employee_id": employee_id,
            "total_leave_days": total_leave_days or 0,
        }
        for employee_id, total_leave_days in results
    ]