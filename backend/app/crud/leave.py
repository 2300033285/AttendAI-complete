from sqlalchemy.orm import Session

from app.models.leave import Leave
from app.schemas.leave import LeaveCreate, LeaveUpdate


def create_leave(
    db: Session,
    employee_id: int,
    leave: LeaveCreate,
):
    db_leave = Leave(
        employee_id=employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="Pending",
    )

    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)

    return db_leave


def get_leave_by_id(
    db: Session,
    leave_id: int,
):
    return (
        db.query(Leave)
        .filter(Leave.id == leave_id)
        .first()
    )


def get_leaves_by_employee(
    db: Session,
    employee_id: int,
):
    return (
        db.query(Leave)
        .filter(Leave.employee_id == employee_id)
        .order_by(Leave.start_date.desc())
        .all()
    )


def get_all_leaves(
    db: Session,
):
    return (
        db.query(Leave)
        .order_by(Leave.start_date.desc())
        .all()
    )


def update_leave_status(
    db: Session,
    leave_id: int,
    leave: LeaveUpdate,
):
    db_leave = (
        db.query(Leave)
        .filter(Leave.id == leave_id)
        .first()
    )

    if db_leave is None:
        return None

    db_leave.status = leave.status

    db.commit()
    db.refresh(db_leave)

    return db_leave