from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.leave import Leave


def get_leave_summary(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(Leave)

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(Leave.start_date >= start_date)

    if end_date is not None:
        query = query.filter(Leave.end_date <= end_date)

    if leave_type is not None:
        query = query.filter(Leave.leave_type == leave_type)

    if status is not None:
        query = query.filter(Leave.status == status)

    total = query.with_entities(func.count(Leave.id)).scalar()

    approved = query.filter(
        Leave.status == "Approved"
    ).with_entities(
        func.count(Leave.id)
    ).scalar()

    rejected = query.filter(
        Leave.status == "Rejected"
    ).with_entities(
        func.count(Leave.id)
    ).scalar()

    pending = query.filter(
        Leave.status == "Pending"
    ).with_entities(
        func.count(Leave.id)
    ).scalar()

    return {
        "total_leaves": total or 0,
        "approved_leaves": approved or 0,
        "rejected_leaves": rejected or 0,
        "pending_leaves": pending or 0,
    }


def get_leave_type_summary(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
):
    query = db.query(
        Leave.leave_type,
        func.count(Leave.id).label("count")
    )

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(Leave.start_date >= start_date)

    if end_date is not None:
        query = query.filter(Leave.end_date <= end_date)

    if status is not None:
        query = query.filter(Leave.status == status)

    return (
        query
        .group_by(Leave.leave_type)
        .all()
    )


def get_employee_leave_summary(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(
        Leave.employee_id,
        func.count(Leave.id).label("leave_count")
    )

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(Leave.start_date >= start_date)

    if end_date is not None:
        query = query.filter(Leave.end_date <= end_date)

    if leave_type is not None:
        query = query.filter(Leave.leave_type == leave_type)

    if status is not None:
        query = query.filter(Leave.status == status)

    return (
        query
        .group_by(Leave.employee_id)
        .all()
    )
def get_monthly_leave_summary(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(
        func.date_trunc("month", Leave.start_date).label("month"),
        func.count(Leave.id).label("leave_count")
    )

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(Leave.start_date >= start_date)

    if end_date is not None:
        query = query.filter(Leave.end_date <= end_date)

    if leave_type is not None:
        query = query.filter(Leave.leave_type == leave_type)

    if status is not None:
        query = query.filter(Leave.status == status)

    return (
        query
        .group_by(func.date_trunc("month", Leave.start_date))
        .order_by(func.date_trunc("month", Leave.start_date))
        .all()
    )
def get_leave_days_summary(
    db: Session,
    employee_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    leave_type: Optional[str] = None,
    status: Optional[str] = None,
):
    query = db.query(
        Leave.employee_id,
        func.sum(
            Leave.end_date - Leave.start_date + 1
        ).label("total_leave_days")
    )

    if employee_id is not None:
        query = query.filter(Leave.employee_id == employee_id)

    if start_date is not None:
        query = query.filter(Leave.start_date >= start_date)

    if end_date is not None:
        query = query.filter(Leave.end_date <= end_date)

    if leave_type is not None:
        query = query.filter(Leave.leave_type == leave_type)

    if status is not None:
        query = query.filter(Leave.status == status)

    return (
        query
        .group_by(Leave.employee_id)
        .order_by(Leave.employee_id)
        .all()
    )