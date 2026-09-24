from pydantic import BaseModel


class ReferralInsightsResponse(BaseModel):
    total_referrals: int
    pending_referrals: int
    reviewed_referrals: int
    rejected_referrals: int
    selected_referrals: int
    selection_rate: float
    pending_rate: float