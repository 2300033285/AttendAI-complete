from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employee import Employee
from app.models.shift import Shift
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


# ==========================================
# VALIDATE SHIFT
# ==========================================

def validate_shift(db: Session, shift_id: int | None):

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
            detail="Shift not found"
        )

    if not shift.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign an inactive shift"
        )


# ==========================================
# CREATE EMPLOYEE
# ==========================================

def create_employee(
    db: Session,
    employee: EmployeeCreate
):

    # Check duplicate employee ID
    existing_employee = (
        db.query(Employee)
        .filter(
            Employee.employee_id == employee.employee_id
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )

    # Check duplicate email
    existing_email = (
        db.query(Employee)
        .filter(
            Employee.email == employee.email.lower()
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee email already exists"
        )

    # Validate shift
    validate_shift(
        db,
        employee.shift_id
    )

    # Create employee
    db_employee = Employee(
        employee_id=employee.employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email.lower(),
        phone=employee.phone,
        department=employee.department,
        designation=employee.designation,
        joining_date=employee.joining_date,
        salary=employee.salary,
        shift_id=employee.shift_id
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


# ==========================================
# GET ALL EMPLOYEES
# ==========================================

def get_all_employees(
    db: Session
):
    return db.query(Employee).all()


# ==========================================
# GET EMPLOYEE BY DATABASE ID
# ==========================================

def get_employee_by_id(
    db: Session,
    employee_id: int
):

    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


# ==========================================
# UPDATE EMPLOYEE
# ==========================================

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

    # Validate shift
    if "shift_id" in update_data:
        validate_shift(
            db,
            update_data["shift_id"]
        )

    # Update fields
    for key, value in update_data.items():

        if key == "email":
            value = value.lower()

        setattr(
            db_employee,
            key,
            value
        )

    db.commit()
    db.refresh(db_employee)

    return db_employee


# ==========================================
# DELETE EMPLOYEE
# ==========================================

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