from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.leave import Leave


def get_leave_report_summary(
    db: Session,
    employee_id: int | None = None,
):
    query = db.query(Leave)

    if employee_id is not None:
        query = query.filter(
            Leave.employee_id == employee_id
        )

    leaves = query.all()

    total_leaves = len(leaves)

    approved_leaves = sum(
        1 for leave in leaves
        if leave.status == "Approved"
    )

    rejected_leaves = sum(
        1 for leave in leaves
        if leave.status == "Rejected"
    )

    pending_leaves = sum(
        1 for leave in leaves
        if leave.status == "Pending"
    )

    total_leave_days = sum(
        (leave.end_date - leave.start_date).days + 1
        for leave in leaves
    )

    return {
        "total_leaves": total_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,
        "pending_leaves": pending_leaves,
        "total_leave_days": total_leave_days,
    }


def get_leave_report_by_employee(
    db: Session,
):
    results = (
        db.query(
            Leave.employee_id,
            func.count(Leave.id).label("total_leaves"),
        )
        .group_by(Leave.employee_id)
        .order_by(Leave.employee_id)
        .all()
    )

    reports = []

    for employee_id, total_leaves in results:

        leaves = (
            db.query(Leave)
            .filter(
                Leave.employee_id == employee_id
            )
            .all()
        )

        approved = sum(
            1 for leave in leaves
            if leave.status == "Approved"
        )

        rejected = sum(
            1 for leave in leaves
            if leave.status == "Rejected"
        )

        pending = sum(
            1 for leave in leaves
            if leave.status == "Pending"
        )

        total_days = sum(
            (leave.end_date - leave.start_date).days + 1
            for leave in leaves
        )

        reports.append({
            "employee_id": employee_id,
            "total_leaves": total_leaves,
            "approved_leaves": approved,
            "rejected_leaves": rejected,
            "pending_leaves": pending,
            "total_leave_days": total_days,
        })

    return reports


def get_leave_report_by_type(
    db: Session,
):
    results = (
        db.query(
            Leave.leave_type,
            func.count(Leave.id).label("total_leaves"),
        )
        .group_by(Leave.leave_type)
        .order_by(Leave.leave_type)
        .all()
    )

    reports = []

    for leave_type, total_leaves in results:

        leaves = (
            db.query(Leave)
            .filter(
                Leave.leave_type == leave_type
            )
            .all()
        )

        total_days = sum(
            (leave.end_date - leave.start_date).days + 1
            for leave in leaves
        )

        approved = sum(
            1 for leave in leaves
            if leave.status == "Approved"
        )

        rejected = sum(
            1 for leave in leaves
            if leave.status == "Rejected"
        )

        pending = sum(
            1 for leave in leaves
            if leave.status == "Pending"
        )

        reports.append({
            "leave_type": leave_type,
            "total_leaves": total_leaves,
            "approved_leaves": approved,
            "rejected_leaves": rejected,
            "pending_leaves": pending,
            "total_leave_days": total_days,
        })

    return reports


def get_monthly_leave_report(
    db: Session,
    year: int | None = None,
):
    query = db.query(
        extract("year", Leave.start_date).label("year"),
        extract("month", Leave.start_date).label("month"),
        func.count(Leave.id).label("total_leaves"),
    )

    if year is not None:
        query = query.filter(
            extract("year", Leave.start_date) == year
        )

    results = (
        query
        .group_by(
            extract("year", Leave.start_date),
            extract("month", Leave.start_date),
        )
        .order_by(
            extract("year", Leave.start_date),
            extract("month", Leave.start_date),
        )
        .all()
    )

    reports = []

    for result in results:

        result_year = int(result.year)
        result_month = int(result.month)

        leaves_query = db.query(Leave).filter(
            extract("year", Leave.start_date)
            == result_year,
            extract("month", Leave.start_date)
            == result_month,
        )

        leaves = leaves_query.all()

        total_days = sum(
            (leave.end_date - leave.start_date).days + 1
            for leave in leaves
        )

        approved = sum(
            1 for leave in leaves
            if leave.status == "Approved"
        )

        rejected = sum(
            1 for leave in leaves
            if leave.status == "Rejected"
        )

        pending = sum(
            1 for leave in leaves
            if leave.status == "Pending"
        )

        reports.append({
            "year": result_year,
            "month": result_month,
            "total_leaves": result.total_leaves,
            "approved_leaves": approved,
            "rejected_leaves": rejected,
            "pending_leaves": pending,
            "total_leave_days": total_days,
        })

    return reports