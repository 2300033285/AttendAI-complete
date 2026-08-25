from pydantic import BaseModel
from datetime import date, time


class QRAttendanceScan(BaseModel):
    qr_token: str


class QRAttendanceResponse(BaseModel):
    message: str
    employee_id: int
    user_id: int
    attendance_id: int
    date: date
    check_in: time
    check_out: time | None
    status: str
    qr_attendance_id: int