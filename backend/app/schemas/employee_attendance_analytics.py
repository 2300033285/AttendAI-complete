from pydantic import BaseModel


class EmployeeAttendanceAnalyticsResponse(BaseModel):

    employee_id: int
    total_records: int
    present_days: int
    absent_days: int
    late_count: int
    attendance_percentage: float
    average_hours: float