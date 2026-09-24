from typing import List

from pydantic import BaseModel


class ReferralAnomalyResponse(BaseModel):
    employee_id: int
    anomaly_detected: bool
    anomaly_score: int
    severity: str
    total_referrals: int
    pending_referrals: int
    rejected_referrals: int
    anomalies: List[str]