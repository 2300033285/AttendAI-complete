from datetime import date, datetime

from sqlalchemy.orm import Session

from app.crud.leave import (
    create_leave,
    get_leaves_by_employee,
    get_all_leaves,
)

from app.schemas.leave import LeaveCreate
from app.models.leave import Leave


# ============================================================
# APPLY LEAVE
# ============================================================

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

    # Create leave
    created_leave = create_leave(
        db,
        employee_id,
        leave,
    )

    return created_leave, None


# ============================================================
# GET EMPLOYEE LEAVES
# ============================================================

def get_employee_leaves_service(
    db: Session,
    employee_id: int,
):
    return get_leaves_by_employee(
        db,
        employee_id,
    )


# ============================================================
# GET ALL LEAVES
# ============================================================

def get_all_leaves_service(
    db: Session,
):
    return get_all_leaves(db)


# ============================================================
# APPROVE / REJECT LEAVE BY EMPLOYEE ID
# ============================================================

def update_leave_status_by_employee_service(
    db: Session,
    employee_id: int,
    status: str,
):
    # Validate status
    if status not in ["Approved", "Rejected"]:
        return None, "Status must be Approved or Rejected."

    # Find the employee's pending leave
    leave = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Pending",
        )
        .order_by(
            Leave.start_date.asc()
        )
        .first()
    )

    # No pending leave
    if leave is None:
        return None, "No pending leave found for this employee."

    # Update status
    leave.status = status
    leave.reviewed_at = datetime.now()

    db.commit()
    db.refresh(leave)

    return leave, None