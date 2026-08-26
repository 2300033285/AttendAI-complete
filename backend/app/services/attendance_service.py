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