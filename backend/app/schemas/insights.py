from pydantic import BaseModel
from typing import Dict, Any


class InsightsResponse(BaseModel):
    total_employees: int
    active_employees: int
    attendance_percentage: float

    department_summary: Dict[str, int]
    designation_summary: Dict[str, int]

    shift_analytics: Dict[str, Any]
    anomalies: Dict[str, Any]
    ai_prediction: Dict[str, Any]