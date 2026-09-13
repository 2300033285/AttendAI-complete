from typing import Dict
from pydantic import BaseModel


class LeaveAIFeaturesResponse(BaseModel):
    employee_id: int

    total_leave_requests: int
    approved_leave_count: int
    rejected_leave_count: int
    pending_leave_count: int

    total_leave_days: int
    average_leave_duration: float
    short_leave_count: int

    leave_type_counts: Dict[str, int]

    anomaly_score: int
    anomaly_severity: str
    anomaly_detected: bool