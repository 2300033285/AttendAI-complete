from pydantic import BaseModel


class ReferralAnalyticsResponse(BaseModel):
    total_referrals: int
    pending_referrals: int
    reviewed_referrals: int
    rejected_referrals: int
    selected_referrals: int


class OpeningReferralAnalytics(BaseModel):
    opening_id: int
    referral_count: int


class EmployeeReferralAnalytics(BaseModel):
    employee_id: int
    referral_count: int