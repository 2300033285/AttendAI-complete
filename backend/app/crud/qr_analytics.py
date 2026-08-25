from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.qr_attendance import QRAttendance


def get_qr_analytics(db: Session):

    records = db.query(QRAttendance).all()

    if not records:
        return {
            "total_scans": 0,
            "present_scans": 0,
            "other_status_scans": 0,
            "attendance_percentage": 0,
            "unique_employees": 0,
            "average_scans_per_employee": 0,
        }

    total_scans = len(records)

    present_scans = sum(
        1
        for record in records
        if record.status
        and record.status.lower() == "present"
    )

    other_status_scans = total_scans - present_scans

    attendance_percentage = (
        (present_scans / total_scans) * 100
        if total_scans > 0
        else 0
    )

    unique_employees = len(
        set(record.employee_id for record in records)
    )

    average_scans_per_employee = (
        total_scans / unique_employees
        if unique_employees > 0
        else 0
    )

    return {
        "total_scans": total_scans,
        "present_scans": present_scans,
        "other_status_scans": other_status_scans,
        "attendance_percentage": round(attendance_percentage, 2),
        "unique_employees": unique_employees,
        "average_scans_per_employee": round(
            average_scans_per_employee, 2
        ),
    }


def get_daily_qr_analytics(db: Session):

    return (
        db.query(
            func.date(QRAttendance.scanned_at).label("scan_date"),

            func.count(QRAttendance.id).label("total_scans"),

            func.sum(
                case(
                    (QRAttendance.status == "Present", 1),
                    else_=0
                )
            ).label("present_scans"),

            func.sum(
                case(
                    (QRAttendance.status != "Present", 1),
                    else_=0
                )
            ).label("other_status_scans"),
        )
        .group_by(func.date(QRAttendance.scanned_at))
        .order_by(func.date(QRAttendance.scanned_at).desc())
        .all()
    )

def get_employee_qr_analytics(db: Session):

    return (
        db.query(
            QRAttendance.employee_id,

            func.count(QRAttendance.id).label("total_scans"),

            func.sum(
                case(
                    (QRAttendance.status == "Present", 1),
                    else_=0
                )
            ).label("present_scans"),

            func.sum(
                case(
                    (QRAttendance.status != "Present", 1),
                    else_=0
                )
            ).label("other_status_scans"),
        )
        .group_by(QRAttendance.employee_id)
        .order_by(QRAttendance.employee_id)
        .all()
    )