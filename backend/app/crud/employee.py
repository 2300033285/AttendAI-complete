from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.models.shift import Shift
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def validate_shift(db: Session, shift_id: int | None):
    """
    Validate that the shift exists and is active.
    """

    if shift_id is None:
        return

    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    if not shift.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign an inactive shift",
        )


def create_employee(
    db: Session,
    employee: EmployeeCreate
):
    # Validate shift before creating employee
    validate_shift(db, employee.shift_id)

    db_employee = Employee(
        **employee.model_dump()
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_all_employees(
    db: Session
):
    return db.query(Employee).all()


def get_employee_by_id(
    db: Session,
    employee_id: int
):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    db_employee = get_employee_by_id(
        db,
        employee_id
    )

    if not db_employee:
        return None

    update_data = employee.model_dump(
        exclude_unset=True
    )

    # Validate shift only when shift_id is being changed
    if "shift_id" in update_data:
        validate_shift(
            db,
            update_data["shift_id"]
        )

    for key, value in update_data.items():
        setattr(
            db_employee,
            key,
            value
        )

    db.commit()
    db.refresh(db_employee)

    return db_employee


def delete_employee(
    db: Session,
    employee_id: int
):
    db_employee = get_employee_by_id(
        db,
        employee_id
    )

    if not db_employee:
        return None

    db.delete(db_employee)
    db.commit()

    return db_employee
