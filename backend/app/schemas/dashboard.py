from datetime import date, time
from typing import Optional

from pydantic import BaseModel


# ============================================================
# EMPLOYEE DASHBOARD SCHEMAS
# ============================================================

class EmployeeRecentAttendance(BaseModel):
    date: date
    status: str
    check_in: Optional[time] = None
    check_out: Optional[time] = None


class EmployeeAttendanceDashboard(BaseModel):
    today_status: str
    login_time: Optional[time] = None
    check_out_time: Optional[time] = None
    attendance_percentage: float
    recent_attendance: list[EmployeeRecentAttendance]


class EmployeeLeaveDashboard(BaseModel):
    pending: int
    approved: int
    rejected: int


class EmployeeReferralDashboard(BaseModel):
    pending: int
    accepted: int
    rejected: int


class EmployeeDashboardResponse(BaseModel):
    role: str
    attendance: EmployeeAttendanceDashboard
    leave: EmployeeLeaveDashboard
    referrals: EmployeeReferralDashboard


# ============================================================
# ADMIN DASHBOARD SCHEMA
# ============================================================

class AdminDashboardResponse(BaseModel):
    role: str

    total_employees: int
    active_employees: int

    total_attendance: int
    present: int
    absent: int
    late: int

    today_present: int
    today_absent: int
    today_late: int

    total_leaves: int
    pending_leaves: int
    approved_leaves: int
    rejected_leaves: int

    openings: int

    total_referrals: int
    pending_referrals: int
    accepted_referrals: int