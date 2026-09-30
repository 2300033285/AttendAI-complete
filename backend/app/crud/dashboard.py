from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.opening import Opening
from app.models.referral import Referral


def get_admin_dashboard_stats(db: Session):

    # ---------------------------------------------------------
    # Employee Statistics
    # ---------------------------------------------------------

    total_employees = (
        db.query(Employee)
        .count()
    )

    active_employees = (
        db.query(Employee)
        .filter(Employee.status.is_(True))
        .count()
    )

    # ---------------------------------------------------------
    # Overall Attendance Statistics
    # ---------------------------------------------------------

    total_attendance = (
        db.query(Attendance)
        .count()
    )

    present = (
        db.query(Attendance)
        .filter(Attendance.status == "Present")
        .count()
    )

    absent = (
        db.query(Attendance)
        .filter(Attendance.status == "Absent")
        .count()
    )

    late = (
        db.query(Attendance)
        .filter(Attendance.status == "Late")
        .count()
    )

    # ---------------------------------------------------------
    # Today's Attendance Statistics
    # ---------------------------------------------------------

    today_present = (
        db.query(Attendance)
        .filter(
            Attendance.date == func.current_date(),
            Attendance.status == "Present"
        )
        .count()
    )

    today_absent = (
        db.query(Attendance)
        .filter(
            Attendance.date == func.current_date(),
            Attendance.status == "Absent"
        )
        .count()
    )

    today_late = (
        db.query(Attendance)
        .filter(
            Attendance.date == func.current_date(),
            Attendance.status == "Late"
        )
        .count()
    )

    # ---------------------------------------------------------
    # Leave Statistics
    # ---------------------------------------------------------

    total_leaves = (
        db.query(Leave)
        .count()
    )

    pending_leaves = (
        db.query(Leave)
        .filter(Leave.status == "Pending")
        .count()
    )

    approved_leaves = (
        db.query(Leave)
        .filter(Leave.status == "Approved")
        .count()
    )

    rejected_leaves = (
        db.query(Leave)
        .filter(Leave.status == "Rejected")
        .count()
    )

    # ---------------------------------------------------------
    # Job Opening Statistics
    # ---------------------------------------------------------

    openings = (
        db.query(Opening)
        .filter(Opening.status == "Open")
        .count()
    )

    # ---------------------------------------------------------
    # Referral Statistics
    # ---------------------------------------------------------

    total_referrals = (
        db.query(Referral)
        .count()
    )

    pending_referrals = (
        db.query(Referral)
        .filter(Referral.status == "Pending")
        .count()
    )

    accepted_referrals = (
        db.query(Referral)
        .filter(Referral.status == "Accepted")
        .count()
    )

    # ---------------------------------------------------------
    # Dashboard Response
    # ---------------------------------------------------------

    return {
        "role": "Admin",

        "total_employees": total_employees,
        "active_employees": active_employees,

        "total_attendance": total_attendance,
        "present": present,
        "absent": absent,
        "late": late,

        "today_present": today_present,
        "today_absent": today_absent,
        "today_late": today_late,

        "total_leaves": total_leaves,
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,

        "openings": openings,

        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "accepted_referrals": accepted_referrals,
    }


def get_employee_dashboard_stats(
    db: Session,
    user_id: int,
    employee_id: int,
):

    # ---------------------------------------------------------
    # Employee Profile
    # ---------------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    total_employees = 1 if employee else 0

    active_employees = (
        1
        if employee and employee.status
        else 0
    )

    # ---------------------------------------------------------
    # Employee Attendance Statistics
    # ---------------------------------------------------------

    total_attendance = (
        db.query(Attendance)
        .filter(Attendance.user_id == user_id)
        .count()
    )

    present = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.status == "Present"
        )
        .count()
    )

    absent = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.status == "Absent"
        )
        .count()
    )

    late = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.status == "Late"
        )
        .count()
    )

    # ---------------------------------------------------------
    # Today's Employee Attendance
    # ---------------------------------------------------------

    today_present = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == func.current_date(),
            Attendance.status == "Present"
        )
        .count()
    )

    today_absent = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == func.current_date(),
            Attendance.status == "Absent"
        )
        .count()
    )

    today_late = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == func.current_date(),
            Attendance.status == "Late"
        )
        .count()
    )

    # ---------------------------------------------------------
    # Employee Leave Statistics
    # ---------------------------------------------------------

    total_leaves = (
        db.query(Leave)
        .filter(Leave.employee_id == employee_id)
        .count()
    )

    pending_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Pending"
        )
        .count()
    )

    approved_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Approved"
        )
        .count()
    )

    rejected_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Rejected"
        )
        .count()
    )

    # ---------------------------------------------------------
    # Available Job Openings
    # ---------------------------------------------------------

    openings = (
        db.query(Opening)
        .filter(Opening.status == "Open")
        .count()
    )

    # ---------------------------------------------------------
    # Employee Referral Statistics
    # ---------------------------------------------------------

    total_referrals = (
        db.query(Referral)
        .filter(Referral.employee_id == employee_id)
        .count()
    )

    pending_referrals = (
        db.query(Referral)
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Pending"
        )
        .count()
    )

    accepted_referrals = (
        db.query(Referral)
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Accepted"
        )
        .count()
    )

    # ---------------------------------------------------------
    # Dashboard Response
    # ---------------------------------------------------------

    return {
        "role": "Employee",

        "total_employees": total_employees,
        "active_employees": active_employees,

        "total_attendance": total_attendance,
        "present": present,
        "absent": absent,
        "late": late,

        "today_present": today_present,
        "today_absent": today_absent,
        "today_late": today_late,

        "total_leaves": total_leaves,
        "pending_leaves": pending_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,

        "openings": openings,

        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "accepted_referrals": accepted_referrals,
    }