from pydantic import BaseModel
from datetime import datetime


class QRAttendanceScan(BaseModel):
    qr_token: str


class QRAttendanceResponse(BaseModel):
    id: int
    employee_id: int
    qr_token: str
    scanned_at: datetime
    status: str

    class Config:
        from_attributes = True