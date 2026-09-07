from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AttendanceCreate(BaseModel):
    user_id: int
    date: date
    check_in: time
    check_out: time
    status: str


class AttendanceUpdate(BaseModel):
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    date: date
    check_in: Optional[time]
    check_out: Optional[time]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceHistoryResponse(BaseModel):
    attendance_id: int
    user_id: int
    employee_id: int | None = None
    employee_name: str | None = None
    email: str | None = None
    date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
        
class AttendanceReportResponse(BaseModel):
    employee_id: int
    user_id: int
    employee_name: str | None = None
    email: str | None = None

    start_date: date
    end_date: date

    total_days: int
    total_attendance_records: int
    present_days: int
    absent_days: int
    attendance_percentage: float