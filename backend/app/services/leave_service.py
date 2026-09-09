from datetime import date, datetime

from sqlalchemy.orm import Session

from app.crud.leave import (
    create_leave,
    get_leave_by_id,
    get_leaves_by_employee,
    get_all_leaves,
    update_leave_status,
)

from app.schemas.leave import LeaveCreate, LeaveUpdate
from app.models.leave import Leave


def apply_leave_service(
    db: Session,
    employee_id: int,
    leave: LeaveCreate,
):
    # Validate date range
    if leave.start_date > leave.end_date:
        return None, "Start date cannot be greater than end date."

    # Prevent applying for a past date
    if leave.start_date < date.today():
        return None, "Leave cannot be applied for a past date."

    # Check for overlapping leave
    overlapping_leave = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status != "Rejected",
            Leave.start_date <= leave.end_date,
            Leave.end_date >= leave.start_date,
        )
        .first()
    )

    if overlapping_leave:
        return None, "Leave dates overlap with an existing leave."

    created_leave = create_leave(
        db,
        employee_id,
        leave,
    )

    return created_leave, None


def get_employee_leaves_service(
    db: Session,
    employee_id: int,
):
    return get_leaves_by_employee(
        db,
        employee_id,
    )


def get_all_leaves_service(
    db: Session,
):
    return get_all_leaves(db)


def get_leave_service(
    db: Session,
    leave_id: int,
):
    return get_leave_by_id(
        db,
        leave_id,
    )


def update_leave_status_service(
    db: Session,
    leave_id: int,
    status: str,
):
    leave = get_leave_by_id(
        db,
        leave_id,
    )

    if leave is None:
        return None, "Leave not found."

    if leave.status != "Pending":
        return None, "Only pending leaves can be approved or rejected."

    if status not in ["Approved", "Rejected"]:
        return None, "Status must be Approved or Rejected."

    leave_update = LeaveUpdate(
        status=status
    )

    updated_leave = update_leave_status(
        db,
        leave_id,
        leave_update,
    )

    if updated_leave:
        updated_leave.reviewed_at = datetime.now()

        db.commit()
        db.refresh(updated_leave)

    return updated_leave, None