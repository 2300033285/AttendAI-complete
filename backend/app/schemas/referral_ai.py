from pydantic import BaseModel


class ReferralAIResponse(BaseModel):
    employee_id: int

    total_referrals: int
    pending_referrals: int
    reviewed_referrals: int
    rejected_referrals: int
    selected_referrals: int

    selection_rate: float
    rejection_rate: float
    review_rate: float

    performance_category: str