from datetime import date, datetime

from sqlalchemy.orm import Session

from app.crud.attendance import (
    create_attendance,
    get_all_attendance,
    get_attendance_by_id,
    update_attendance,
    delete_attendance,
)

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
)

from app.models.attendance import Attendance
from app.models.user import User
from app.models.employee import Employee


def create_attendance_service(db: Session, attendance: AttendanceCreate):
    return create_attendance(db, attendance)


def get_all_attendance_service(db: Session):
    return get_all_attendance(db)


def get_attendance_service(db: Session, attendance_id: int):
    return get_attendance_by_id(db, attendance_id)


def update_attendance_service(
    db: Session,
    attendance_id: int,
    attendance: AttendanceUpdate,
):
    return update_attendance(db, attendance_id, attendance)


def delete_attendance_service(
    db: Session,
    attendance_id: int,
):
    return delete_attendance(db, attendance_id)


def check_in_service(db: Session, user_id: int):
    today = date.today()
    current_time = datetime.now().time()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == today,
        )
        .first()
    )

    if attendance:
        if attendance.check_in is not None:
            return None, "Employee already checked in today."

        attendance.check_in = current_time
        attendance.status = "Present"

    else:
        attendance = Attendance(
            user_id=user_id,
            date=today,
            check_in=current_time,
            status="Present",
        )
        db.add(attendance)

    db.commit()
    db.refresh(attendance)

    return attendance, None


def check_out_service(db: Session, user_id: int):
    today = date.today()
    current_time = datetime.now().time()

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == today,
        )
        .first()
    )

    if attendance is None:
        return None, "No check-in record found for today."

    if attendance.check_in is None:
        return None, "Employee has not checked in."

    if attendance.check_out is not None:
        return None, "Employee already checked out today."

    attendance.check_out = current_time

    # Handle existing attendance records
    # that may have NULL created_at.
    if attendance.created_at is None:
        attendance.created_at = datetime.now()

    db.commit()
    db.refresh(attendance)

    return attendance, None


# ============================================================
# ATTENDANCE HISTORY SERVICE
# ============================================================

def get_attendance_history_service(
    db: Session,
    user_id: int | None = None,
    employee_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
):
    query = (
        db.query(Attendance, User, Employee)
        .join(
            User,
            Attendance.user_id == User.id,
        )
        .outerjoin(
            Employee,
            Employee.email == User.email,
        )
    )

    # Filter by user
    if user_id is not None:
        query = query.filter(
            Attendance.user_id == user_id
        )

    # Filter by employee
    if employee_id is not None:
        query = query.filter(
            Employee.id == employee_id
        )

    # Filter by starting date
    if start_date is not None:
        query = query.filter(
            Attendance.date >= start_date
        )

    # Filter by ending date
    if end_date is not None:
        query = query.filter(
            Attendance.date <= end_date
        )

    # Latest attendance first
    records = (
        query
        .order_by(Attendance.date.desc())
        .all()
    )

    result = []

    for attendance, user, employee in records:

        employee_name = None

        if employee:
            employee_name = (
                f"{employee.first_name} "
                f"{employee.last_name}"
            )

        result.append({
            "attendance_id": attendance.id,
            "user_id": attendance.user_id,
            "employee_id": employee.id if employee else None,
            "employee_name": employee_name,
            "email": user.email,
            "date": attendance.date,
            "check_in": attendance.check_in,
            "check_out": attendance.check_out,
            "status": attendance.status,
            "created_at": attendance.created_at,
        })

    return result

# ============================================================
# ATTENDANCE REPORT SERVICE
# ============================================================

def get_attendance_report_service(
    db: Session,
    user_id: int,
    employee_id: int,
    start_date: date,
    end_date: date,
):
    # Get attendance records for the selected employee
    records = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date,
        )
        .order_by(Attendance.date.asc())
        .all()
    )

    # Get employee details
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    # Get user details
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    # Total days in selected date range
    total_days = (end_date - start_date).days + 1

    # Count present days
    present_days = sum(
        1
        for record in records
        if record.status == "Present"
    )

    # Days without attendance records
    absent_days = total_days - present_days

    # Calculate attendance percentage
    attendance_percentage = (
        (present_days / total_days) * 100
        if total_days > 0
        else 0
    )

    # Employee name
    employee_name = None

    if employee:
        employee_name = (
            f"{employee.first_name} "
            f"{employee.last_name}"
        )

    return {
        "employee_id": employee_id,
        "user_id": user_id,
        "employee_name": employee_name,
        "email": user.email if user else None,
        "start_date": start_date,
        "end_date": end_date,
        "total_days": total_days,
        "total_attendance_records": len(records),
        "present_days": present_days,
        "absent_days": absent_days,
        "attendance_percentage": round(
            attendance_percentage,
            2,
        ),
    }