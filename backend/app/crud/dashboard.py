from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.leave import Leave
from app.models.opening import Opening
from app.models.referral import Referral


# ============================================================
# ADMIN DASHBOARD
# ============================================================

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
    # Attendance Statistics
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
    # Today's Attendance
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


# ============================================================
# EMPLOYEE DASHBOARD
# ============================================================

def get_employee_dashboard_stats(
    db: Session,
    user_id: int,
    employee_id: int,
):

    # ---------------------------------------------------------
    # Verify Employee
    # ---------------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None

    # ---------------------------------------------------------
    # Today's Attendance
    # ---------------------------------------------------------

    today_attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.date == func.current_date(),
        )
        .first()
    )

    if today_attendance:
        today_status = today_attendance.status
        login_time = today_attendance.check_in
        check_out_time = today_attendance.check_out
    else:
        today_status = "Not Checked In"
        login_time = None
        check_out_time = None

    # ---------------------------------------------------------
    # Attendance Percentage
    # ---------------------------------------------------------

    total_attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id
        )
        .count()
    )

    present_days = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.status == "Present",
        )
        .count()
    )

    attendance_percentage = (
        round(
            (present_days / total_attendance) * 100,
            2,
        )
        if total_attendance > 0
        else 0.0
    )

    # ---------------------------------------------------------
    # Recent Attendance
    # ---------------------------------------------------------

    recent_records = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id
        )
        .order_by(
            Attendance.date.desc(),
            Attendance.id.desc(),
        )
        .limit(5)
        .all()
    )

    recent_attendance = [
        {
            "date": record.date,
            "status": record.status,
            "check_in": record.check_in,
            "check_out": record.check_out,
        }
        for record in recent_records
    ]

    # ---------------------------------------------------------
    # Leave Statistics
    # ---------------------------------------------------------

    pending_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Pending",
        )
        .count()
    )

    approved_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Approved",
        )
        .count()
    )

    rejected_leaves = (
        db.query(Leave)
        .filter(
            Leave.employee_id == employee_id,
            Leave.status == "Rejected",
        )
        .count()
    )

    # ---------------------------------------------------------
    # Referral Statistics
    # ---------------------------------------------------------

    pending_referrals = (
        db.query(Referral)
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Pending",
        )
        .count()
    )

    accepted_referrals = (
        db.query(Referral)
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Accepted",
        )
        .count()
    )

    rejected_referrals = (
        db.query(Referral)
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Rejected",
        )
        .count()
    )

    # ---------------------------------------------------------
    # Employee Dashboard Response
    # ---------------------------------------------------------

    return {
        "role": "Employee",

        "attendance": {
            "today_status": today_status,
            "login_time": login_time,
            "check_out_time": check_out_time,
            "attendance_percentage": attendance_percentage,
            "recent_attendance": recent_attendance,
        },

        "leave": {
            "pending": pending_leaves,
            "approved": approved_leaves,
            "rejected": rejected_leaves,
        },

        "referrals": {
            "pending": pending_referrals,
            "accepted": accepted_referrals,
            "rejected": rejected_referrals,
        },
    }