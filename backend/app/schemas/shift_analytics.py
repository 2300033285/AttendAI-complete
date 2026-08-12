from pydantic import BaseModel
from typing import Dict


class ShiftAnalyticsResponse(BaseModel):
    total_shifts: int
    completed_shifts: int
    missed_shifts: int
    average_shift_hours: float
    overtime_hours: float
    shift_wise_attendance: Dict[str, Dict[str, int]]