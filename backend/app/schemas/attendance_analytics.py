from pydantic import BaseModel


class AttendanceAnalyticsResponse(BaseModel):
    attendance_percentage: float
    present_days: int
    absent_days: int
    late_count: int
    average_hours: float