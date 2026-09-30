from pydantic import BaseModel


class DashboardResponse(BaseModel):
    role: str

    # Employee statistics
    total_employees: int
    active_employees: int

    # Attendance statistics
    total_attendance: int
    present: int
    absent: int
    late: int

    # Today's attendance
    today_present: int
    today_absent: int
    today_late: int

    # Leave statistics
    total_leaves: int
    pending_leaves: int
    approved_leaves: int
    rejected_leaves: int

    # Job openings
    openings: int

    # Referral statistics
    total_referrals: int
    pending_referrals: int
    accepted_referrals: int